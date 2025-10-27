import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.routes import router
from backend.config.config import set_env_variables

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
    """Health check endpoint"""
    try:
        print("📥 [app.py:health_check] Health check accessed")
        return {"status": "healthy"}
    except Exception as e:
        print(f"❌ [app.py:health_check] Error in health check: {str(e)}")
        traceback.print_exc()
        raise

if __name__ == "__main__":
    try:
        import uvicorn
        print("🚀 [app.py] Starting uvicorn server")
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        print(f"❌ [app.py] Error starting server: {str(e)}")
        traceback.print_exc()
        raise
