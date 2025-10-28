import asyncio
import os
import traceback
from typing import AsyncGenerator
from google.genai import types
from backend.services.memory.memory import memory_store

async def chat_stream(message: str, session_id: str, role: str = "general") -> AsyncGenerator[str, None]:
    """
    Stream chat response with memory
    
    Args:
        message: User's message
        session_id: Session ID for maintaining conversation history
        role: Chatbot role (general, doctor, programmer)
    
    Yields:
        Streaming tokens from the LLM
    """
    try:
        print(f"🚀 [services/chat/chat.py:chat_stream] Starting chat_stream with session_id={session_id}, role={role}")
        
        from backend.services.llm_connector.llm_connector import load_llm, get_grounding_tool
        from backend.prompts.prompts import general_system_prompt, doctor_system_prompt, programmer_system_prompt
        
        # Load LLM client
        try:
            client = load_llm()
        except Exception as e:
            print(f"❌ [services/chat/chat.py:chat_stream] Error loading LLM client: {str(e)}")
            traceback.print_exc()
            raise
        
        # Get appropriate system prompt
        try:
            prompts = {
                "general": general_system_prompt,
                "doctor": doctor_system_prompt,
                "programmer": programmer_system_prompt
            }
            system_prompt = prompts.get(role, general_system_prompt)
            print(f"✅ [services/chat/chat.py:chat_stream] Using role={role}, system_prompt length={len(system_prompt)}")
        except Exception as e:
            print(f"❌ [services/chat/chat.py:chat_stream] Error getting system prompt: {str(e)}")
            traceback.print_exc()
            raise
        
        # Get conversation history
        try:
            history = memory_store.get_conversation_history(session_id)
            print(f"✅ [services/chat/chat.py:chat_stream] Retrieved history with {len(history)} messages")
        except Exception as e:
            print(f"❌ [services/chat/chat.py:chat_stream] Error getting conversation history: {str(e)}")
            traceback.print_exc()
            history = []
        
        # Add system prompt and user message
        try:
            contents = [
                {
                    "role": "user",
                    "parts": [{"text": system_prompt}]
                },
                {
                    "role": "model",
                    "parts": [{"text": "I understand. How can I help you today?"}]
                }
            ]
            
            # Add conversation history
            contents.extend(history)
            
            # Add current user message
            contents.append({
                "role": "user",
                "parts": [{"text": message}]
            })
            print(f"✅ [services/chat/chat.py:chat_stream] Prepared contents with {len(contents)} messages")
        except Exception as e:
            print(f"❌ [services/chat/chat.py:chat_stream] Error preparing contents: {str(e)}")
            traceback.print_exc()
            raise
        
        # Save user message to memory
        try:
            memory_store.add_message(session_id, {
                "role": "user",
                "content": message
            })
            print(f"✅ [services/chat/chat.py:chat_stream] Saved user message to memory")
        except Exception as e:
            print(f"❌ [services/chat/chat.py:chat_stream] Error saving user message to memory: {str(e)}")
            traceback.print_exc()
            # Don't raise, continue anyway
        
        # Setup grounding tool
        try:
            grounding_tool = get_grounding_tool()
            config = types.GenerateContentConfig(tools=[grounding_tool])
            print(f"✅ [services/chat/chat.py:chat_stream] Created grounding tool and config")
        except Exception as e:
            print(f"❌ [services/chat/chat.py:chat_stream] Error setting up grounding tool: {str(e)}")
            traceback.print_exc()
            raise
        
        # Get model (required)
        try:
            model_name = os.environ["GEMINI_MODEL"]
            print(f"✅ [services/chat/chat.py:chat_stream] Using model (GEMINI_MODEL): {model_name}")
        except KeyError:
            error_msg = "GEMINI_MODEL environment variable is required but not set"
            print(f"❌ [services/chat/chat.py:chat_stream] {error_msg}")
            raise ValueError(error_msg)
        
        try:
            # Stream response
            print(f"🔄 [services/chat/chat.py:chat_stream] Starting to stream response from model")
            response = client.models.generate_content_stream(
                model=model_name,
                contents=contents,
                config=config,
            )
            
            full_response = ""
            chunk_count = 0
            for chunk in response:
                try:
                    if chunk.text:
                        full_response += chunk.text
                        chunk_count += 1
                        yield chunk.text
                except Exception as e:
                    print(f"❌ [services/chat/chat.py:chat_stream] Error processing chunk: {str(e)}")
                    traceback.print_exc()
            
            print(f"✅ [services/chat/chat.py:chat_stream] Streamed {chunk_count} chunks, total length: {len(full_response)}")
            
            # Save assistant's response to memory
            if full_response:
                try:
                    memory_store.add_message(session_id, {
                        "role": "model",
                        "content": full_response
                    })
                    print(f"✅ [services/chat/chat.py:chat_stream] Saved assistant response to memory")
                except Exception as e:
                    print(f"❌ [services/chat/chat.py:chat_stream] Error saving assistant response to memory: {str(e)}")
                    traceback.print_exc()
                    # Don't raise, response is already yielded
        
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(f"❌ [services/chat/chat.py:chat_stream] Error during streaming: {error_msg}")
            traceback.print_exc()
            yield error_msg
            raise
    
    except Exception as e:
        print(f"❌ [services/chat/chat.py:chat_stream] Unexpected error in chat_stream: {str(e)}")
        traceback.print_exc()
        raise

async def chat(message: str, session_id: str, role: str = "general") -> str:
    """
    Non-streaming chat response with memory
    
    Args:
        message: User's message
        session_id: Session ID for maintaining conversation history
        role: Chatbot role (general, doctor, programmer)
    
    Returns:
        Complete response from the LLM
    """
    try:
        print(f"🚀 [services/chat/chat.py:chat] Starting non-streaming chat")
        response_text = ""
        chunk_count = 0
        async for chunk in chat_stream(message, session_id, role):
            try:
                response_text += chunk
                chunk_count += 1
            except Exception as e:
                print(f"❌ [services/chat/chat.py:chat] Error processing chunk in non-streaming mode: {str(e)}")
                traceback.print_exc()
        
        print(f"✅ [services/chat/chat.py:chat] Completed with {chunk_count} chunks, total length: {len(response_text)}")
        return response_text
    except Exception as e:
        print(f"❌ [services/chat/chat.py:chat] Unexpected error in chat: {str(e)}")
        traceback.print_exc()
        raise