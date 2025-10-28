import os
import time
import traceback
from typing import Dict, Any, Tuple

import httpx

from backend.services.memory.memory import memory_store


def check_environment() -> Dict[str, Any]:
    """Check required environment configuration."""
    try:
        google_api_key = os.getenv("GOOGLE_API_KEY")
        model = os.environ.get("GEMINI_MODEL")
        status = "healthy" if google_api_key else "degraded"
        result = {
            "status": status,
            "details": {
                "google_api_key_set": bool(google_api_key),
                "model": model,
                "api_key_length": len(google_api_key) if google_api_key else 0,
            },
        }
        if not google_api_key:
            result["error"] = "GOOGLE_API_KEY not set"
        if not model:
            result["model_error"] = "GEMINI_MODEL not set"
        return result
    except Exception as e:
        print(f"❌ [services/health/health.py:check_environment] {str(e)}")
        traceback.print_exc()
        return {"status": "unhealthy", "error": str(e)}


def check_memory_service() -> Dict[str, Any]:
    """Exercise memory store: add, get, clear."""
    try:
        test_session = "health-check-test"
        memory_store.add_message(test_session, {"role": "system", "content": "Health check"})
        history = memory_store.get_history(test_session)
        memory_store.clear_session(test_session)
        return {
            "status": "healthy",
            "details": {
                "add_message": "working",
                "get_history": "working",
                "clear_session": "working",
                "active_sessions": len(memory_store._sessions),
                "history_length": len(history),
            },
        }
    except Exception as e:
        print(f"❌ [services/health/health.py:check_memory_service] {str(e)}")
        traceback.print_exc()
        return {"status": "unhealthy", "error": str(e)}


def check_llm_service() -> Dict[str, Any]:
    """Verify LLM client loads and grounding tool can be created."""
    try:
        from backend.services.llm_connector.llm_connector import load_llm, get_grounding_tool

        client = load_llm()
        tool = get_grounding_tool()
        return {
            "status": "healthy",
            "details": {
                "client_loaded": client is not None,
                "grounding_tool_created": tool is not None,
                "model": os.environ.get("GEMINI_MODEL"),
            },
        }
    except Exception as e:
        print(f"❌ [services/health/health.py:check_llm_service] {str(e)}")
        traceback.print_exc()
        return {"status": "degraded", "error": str(e)}


async def deep_check_endpoints(app) -> Dict[str, Any]:
    """Make in-process HTTP calls to exercise API endpoints."""
    try:
        print("🔍 [services/health/health.py:deep_check_endpoints] Starting deep checks")
        deep_results: Dict[str, Any] = {}
        test_session = "health-check-deep"

        # Seed a test message
        memory_store.add_message(test_session, {"role": "user", "content": "ping"})

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test", timeout=10.0) as client:
            # Root
            t0 = time.time()
            resp = await client.get("/")
            deep_results["/"] = {
                "status_code": resp.status_code,
                "ok": resp.is_success,
                "latency_ms": round((time.time() - t0) * 1000, 2),
            }

            # Docs
            t0 = time.time()
            resp = await client.get("/docs")
            deep_results["/docs"] = {
                "status_code": resp.status_code,
                "ok": resp.status_code in (200, 307, 308),
                "latency_ms": round((time.time() - t0) * 1000, 2),
            }

            # Non-streaming chat
            chat_payload = {"message": "health ping", "session_id": test_session, "role": "general"}
            t0 = time.time()
            resp = await client.post("/api/v1/chat", json=chat_payload)
            deep_results["/api/v1/chat"] = {
                "status_code": resp.status_code,
                "ok": resp.is_success,
                "latency_ms": round((time.time() - t0) * 1000, 2),
            }

            # Streaming chat
            try:
                t0 = time.time()
                async with client.stream("POST", "/api/v1/chat/stream", json=chat_payload) as stream_resp:
                    ok = stream_resp.status_code == 200
                    received_any = False
                    async for line in stream_resp.aiter_lines():
                        if line:
                            received_any = True
                            break
                    deep_results["/api/v1/chat/stream"] = {
                        "status_code": stream_resp.status_code,
                        "ok": ok and received_any,
                        "latency_ms": round((time.time() - t0) * 1000, 2),
                    }
            except Exception as se:
                deep_results["/api/v1/chat/stream"] = {"status_code": 0, "ok": False, "error": str(se), "latency_ms": 0}

            # History GET
            t0 = time.time()
            resp = await client.get(f"/api/v1/history/{test_session}")
            deep_results["/api/v1/history/{session_id}"] = {
                "status_code": resp.status_code,
                "ok": resp.is_success,
                "latency_ms": round((time.time() - t0) * 1000, 2),
            }

            # Export all
            t0 = time.time()
            resp = await client.get("/api/v1/export")
            deep_results["/api/v1/export"] = {
                "status_code": resp.status_code,
                "ok": resp.is_success,
                "latency_ms": round((time.time() - t0) * 1000, 2),
            }

            # Export session
            t0 = time.time()
            resp = await client.get(f"/api/v1/export/{test_session}")
            deep_results["/api/v1/export/{session_id}"] = {
                "status_code": resp.status_code,
                "ok": resp.is_success,
                "latency_ms": round((time.time() - t0) * 1000, 2),
            }

            # Clear history
            t0 = time.time()
            resp = await client.post("/api/v1/history/clear", json={"session_id": test_session})
            deep_results["/api/v1/history/clear"] = {
                "status_code": resp.status_code,
                "ok": resp.is_success,
                "latency_ms": round((time.time() - t0) * 1000, 2),
            }

        all_ok = all(item.get("ok") for item in deep_results.values())
        return {"status": "healthy" if all_ok else "unhealthy", "details": deep_results}
    except Exception as e:
        print(f"❌ [services/health/health.py:deep_check_endpoints] {str(e)}")
        traceback.print_exc()
        return {"status": "unhealthy", "error": str(e)}


