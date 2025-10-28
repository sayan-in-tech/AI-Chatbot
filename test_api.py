"""
Quick test script for the FastAPI chatbot
Run this to test the API endpoints
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health check endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_chat():
    """Test non-streaming chat endpoint"""
    print("Testing /api/v1/chat endpoint...")
    data = {
        "message": "Hello! Tell me a fun fact about Python.",
        "session_id": "test-session-1",
        "role": "general"
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result['response'][:200]}...")
    print()

def test_chat_stream():
    """Test streaming chat endpoint"""
    print("Testing /api/v1/chat/stream endpoint...")
    print("(Streaming response will be shown as chunks)")
    print()
    
    data = {
        "message": "What are the benefits of using FastAPI?",
        "session_id": "test-session-2",
        "role": "programmer"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/chat/stream", json=data, stream=True)
    
    print("Streaming chunks:")
    for line in response.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            print(decoded, end='', flush=True)
    print("\n")

def test_history():
    """Test getting chat history"""
    print("Testing /api/v1/history/test-session-1 endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/history/test-session-1")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("AI Chatbot API Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_health()
        test_chat()
        test_chat_stream()
        test_history()
        
        print("=" * 50)
        print("✅ All tests completed!")
        print("=" * 50)
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running:")
        print("   python -m backend.run")
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
