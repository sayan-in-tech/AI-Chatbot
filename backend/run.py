"""
Run script for the AI Chatbot FastAPI application
"""
import traceback

if __name__ == "__main__":
    try:
        from backend.utils.clean_cache import clean_pycache
        import uvicorn
    except ImportError as e:
        print(f"❌ [run.py] Import error: {str(e)}")
        traceback.print_exc()
        raise
    
    try:
        # Clean cache before starting
        print("🔧 [run.py] Cleaning cache...")
        clean_pycache()
    except Exception as e:
        print(f"❌ [run.py] Error cleaning cache: {str(e)}")
        traceback.print_exc()
        # Don't raise, continue anyway
    
    try:
        print("🚀 Starting AI Chatbot API...")
        print("📚 API Documentation: http://127.0.0.1:8000/docs")
        print("❤️  Health Check: http://127.0.0.1:8000/health")
        print()
    except Exception as e:
        print(f"❌ [run.py] Error printing startup messages: {str(e)}")
        traceback.print_exc()
    
    try:
        uvicorn.run(
            "backend.app:app",
            host="127.0.0.1",
            port=8000,
            reload=True  # Auto-reload on code changes
        )
    except Exception as e:
        print(f"❌ [run.py] Error starting uvicorn server: {str(e)}")
        traceback.print_exc()
        raise