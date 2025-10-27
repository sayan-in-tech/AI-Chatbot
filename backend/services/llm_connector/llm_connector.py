import os
import traceback
from google.genai import Client, types

def load_llm():
    """Load and return the Gemini client"""
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ [services/llm_connector/llm_connector.py:load_llm] GOOGLE_API_KEY not found in environment variables")
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        try:
            client = Client(api_key=api_key)
            print(f"✅ [services/llm_connector/llm_connector.py:load_llm] Successfully loaded LLM client")
            return client
        except Exception as e:
            print(f"❌ [services/llm_connector/llm_connector.py:load_llm] Error creating Client with api_key: {str(e)}")
            traceback.print_exc()
            raise
    except ValueError as e:
        print(f"❌ [services/llm_connector/llm_connector.py:load_llm] ValueError: {str(e)}")
        traceback.print_exc()
        raise
    except Exception as e:
        print(f"❌ [services/llm_connector/llm_connector.py:load_llm] Unexpected error loading LLM: {str(e)}")
        traceback.print_exc()
        raise

def get_grounding_tool():
    """Get the Google Search grounding tool"""
    try:
        tool = types.Tool(google_search=types.GoogleSearch())
        print(f"✅ [services/llm_connector/llm_connector.py:get_grounding_tool] Successfully created grounding tool")
        return tool
    except Exception as e:
        print(f"❌ [services/llm_connector/llm_connector.py:get_grounding_tool] Error creating grounding tool: {str(e)}")
        traceback.print_exc()
        raise
