import traceback
import time
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from backend.routes.routes import router
from backend.config.config import set_env_variables
from backend.services.health import (
    check_environment,
    check_memory_service,
    check_llm_service,
    deep_check_endpoints,
)

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
        
        # 1. Environment
        env_result = check_environment()
        checks["environment"] = env_result
        if env_result.get("status") == "degraded" and overall_status == "healthy":
            overall_status = "degraded"
        if env_result.get("status") == "unhealthy":
            overall_status = "unhealthy"
        
        # 2. Memory service
        mem_result = check_memory_service()
        checks["memory_service"] = mem_result
        if mem_result.get("status") != "healthy":
            overall_status = "unhealthy"
        
        # 3. LLM service
        llm_result = check_llm_service()
        checks["llm_service"] = llm_result
        if llm_result.get("status") == "degraded" and overall_status == "healthy":
            overall_status = "degraded"
        if llm_result.get("status") == "unhealthy":
            overall_status = "unhealthy"
        
        # 4. Deep endpoint checks
        deep_result = await deep_check_endpoints(app)
        checks["api_endpoints_deep"] = deep_result
        if deep_result.get("status") != "healthy":
            overall_status = "unhealthy"
        
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
