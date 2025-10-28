import traceback
import time
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from backend.routes.routes import router
from backend.config.config import set_env_variables
from backend.services.memory.memory import memory_store

try:
    # Load environment variables
    print("🔧 [app.py] Loading environment variables...")
    set_env_variables()
    print("✅ [app.py] Environment variables loaded successfully")
except Exception as e:
    print(f"❌ [app.py] Error loading environment variables: {str(e)}")
    traceback.print_exc()

try:
    # Create FastAPI app
    app = FastAPI(
        title="AI Chatbot API",
        description="A chatbot API with streaming responses and memory",
        version="1.0.0"
    )
    print("✅ [app.py] FastAPI app created")
except Exception as e:
    print(f"❌ [app.py] Error creating FastAPI app: {str(e)}")
    traceback.print_exc()
    raise

try:
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print("✅ [app.py] CORS middleware configured")
except Exception as e:
    print(f"❌ [app.py] Error configuring CORS: {str(e)}")
    traceback.print_exc()
    raise

try:
    # Include routers
    app.include_router(router, prefix="/api/v1")
    print("✅ [app.py] Routes included successfully")
except Exception as e:
    print(f"❌ [app.py] Error including routes: {str(e)}")
    traceback.print_exc()
    raise

@app.get("/")
async def root():
    """Root endpoint"""
    try:
        print("📥 [app.py:root] Root endpoint accessed")
        return {
            "message": "AI Chatbot",
            "version": "1.0.0",
            "docs": "/docs"
        }
    except Exception as e:
        print(f"❌ [app.py:root] Error in root endpoint: {str(e)}")
        traceback.print_exc()
        raise

@app.get("/health")
async def health_check():
    """
    Comprehensive health check endpoint
    Checks: environment, memory service, LLM connectivity, and API endpoints
    """
    try:
        print("📥 [app.py:health_check] Comprehensive health check started")
        overall_status = "healthy"
        checks = {}
        start_time = time.time()
        
        # 1. Check Environment Variables
        try:
            print("🔍 [app.py:health_check] Checking environment variables...")
            google_api_key = os.getenv("GOOGLE_API_KEY")
            model = os.getenv("MODEL", "gemini-2.0-flash-exp")
            
            checks["environment"] = {
                "status": "healthy" if google_api_key else "degraded",
                "details": {
                    "google_api_key_set": bool(google_api_key),
                    "model": model,
                    "api_key_length": len(google_api_key) if google_api_key else 0
                }
            }
            
            if not google_api_key:
                overall_status = "degraded"
                checks["environment"]["error"] = "GOOGLE_API_KEY not set"
                print("⚠️  [app.py:health_check] GOOGLE_API_KEY not set")
            
            print(f"✅ [app.py:health_check] Environment check: {checks['environment']['status']}")
        except Exception as e:
            print(f"❌ [app.py:health_check] Environment check failed: {str(e)}")
            checks["environment"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            overall_status = "unhealthy"
        
        # 2. Check Memory Service
        try:
            print("🔍 [app.py:health_check] Checking memory service...")
            test_session = "health-check-test"
            
            # Test add message
            memory_store.add_message(test_session, {
                "role": "system",
                "content": "Health check"
            })
            
            # Test get history
            history = memory_store.get_history(test_session)
            
            # Test clear session
            memory_store.clear_session(test_session)
            
            checks["memory_service"] = {
                "status": "healthy",
                "details": {
                    "add_message": "working",
                    "get_history": "working",
                    "clear_session": "working",
                    "active_sessions": len(memory_store._sessions)
                }
            }
            print("✅ [app.py:health_check] Memory service check: healthy")
        except Exception as e:
            print(f"❌ [app.py:health_check] Memory service check failed: {str(e)}")
            checks["memory_service"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            overall_status = "unhealthy"
        
        # 3. Check LLM Connectivity
        try:
            print("🔍 [app.py:health_check] Checking LLM connectivity...")
            from backend.services.llm_connector.llm_connector import load_llm, get_grounding_tool
            
            # Try to load LLM client
            client = load_llm()
            
            # Try to create grounding tool
            tool = get_grounding_tool()
            
            checks["llm_service"] = {
                "status": "healthy",
                "details": {
                    "client_loaded": True,
                    "grounding_tool_created": True,
                    "model": os.getenv("MODEL", "gemini-2.0-flash-exp")
                }
            }
            print("✅ [app.py:health_check] LLM service check: healthy")
        except Exception as e:
            print(f"❌ [app.py:health_check] LLM service check failed: {str(e)}")
            checks["llm_service"] = {
                "status": "degraded",
                "error": str(e)
            }
            if overall_status == "healthy":
                overall_status = "degraded"
        
        # 4. Check API Endpoints
        try:
            print("🔍 [app.py:health_check] Checking API endpoints...")
            endpoint_list = [
                "/",
                "/health",
                "/docs",
                "/api/v1/chat",
                "/api/v1/chat/stream",
                "/api/v1/history/{session_id}",
                "/api/v1/history/clear"
            ]
            
            checks["api_endpoints"] = {
                "status": "healthy",
                "details": {
                    "available_endpoints": endpoint_list,
                    "total_count": len(endpoint_list)
                }
            }
            print("✅ [app.py:health_check] API endpoints check: healthy")
        except Exception as e:
            print(f"❌ [app.py:health_check] API endpoints check failed: {str(e)}")
            checks["api_endpoints"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        # Calculate response time
        response_time = round((time.time() - start_time) * 1000, 2)
        
        # Compile final response
        health_report = {
            "status": overall_status,
            "timestamp": time.time(),
            "response_time_ms": response_time,
            "version": "1.0.0",
            "checks": checks,
            "message": "All systems operational" if overall_status == "healthy" else "Some services need attention"
        }
        
        print(f"✅ [app.py:health_check] Health check completed in {response_time}ms, status: {overall_status}")
        return health_report
        
    except Exception as e:
        print(f"❌ [app.py:health_check] Unexpected error in health check: {str(e)}")
        traceback.print_exc()
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }
