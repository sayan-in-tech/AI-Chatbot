import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.responses import Response
from fastapi import Query
import json
from pydantic import BaseModel, ValidationError
from typing import Optional
from backend.services.chat.chat import chat_stream, chat
from backend.services.memory.memory import memory_store

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str
    role: Optional[str] = "general"

class ChatResponse(BaseModel):
    response: str

class SessionClearRequest(BaseModel):
    session_id: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Non-streaming chat endpoint"""
    try:
        print(f"📥 [routes/routes.py:chat_endpoint] Received request: session_id={request.session_id}, role={request.role}, message_length={len(request.message)}")
        
        try:
            response = await chat(request.message, request.session_id, request.role)
            print(f"✅ [routes/routes.py:chat_endpoint] Successfully got response of length {len(response)}")
            return ChatResponse(response=response)
        except Exception as e:
            print(f"❌ [routes/routes.py:chat_endpoint] Error calling chat function: {str(e)}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))
    except ValidationError as e:
        print(f"❌ [routes/routes.py:chat_endpoint] Validation error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ [routes/routes.py:chat_endpoint] Unexpected error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """Streaming chat endpoint"""
    try:
        print(f"📥 [routes/routes.py:chat_stream_endpoint] Received streaming request: session_id={request.session_id}, role={request.role}")
        
        async def generate():
            try:
                print(f"🔄 [routes/routes.py:chat_stream_endpoint:generate] Starting stream generation")
                async for chunk in chat_stream(request.message, request.session_id, request.role):
                    try:
                        yield f"data: {chunk}\n\n"
                    except Exception as e:
                        print(f"❌ [routes/routes.py:chat_stream_endpoint:generate] Error yielding chunk: {str(e)}")
                        traceback.print_exc()
                        yield f"data: [ERROR] {str(e)}\n\n"
                        break
                yield "data: [DONE]\n\n"
                print(f"✅ [routes/routes.py:chat_stream_endpoint:generate] Stream completed successfully")
            except Exception as e:
                print(f"❌ [routes/routes.py:chat_stream_endpoint:generate] Error in generate: {str(e)}")
                traceback.print_exc()
                yield f"data: [ERROR] {str(e)}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )
    except ValidationError as e:
        print(f"❌ [routes/routes.py:chat_stream_endpoint] Validation error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except Exception as e:
        print(f"❌ [routes/routes.py:chat_stream_endpoint] Unexpected error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_history(session_id: str):
    """Get chat history for a session"""
    try:
        print(f"📥 [routes/routes.py:get_history] Getting history for session_id={session_id}")
        
        try:
            history = memory_store.get_history(session_id)
            print(f"✅ [routes/routes.py:get_history] Retrieved {len(history)} messages")
            return {"session_id": session_id, "history": history}
        except Exception as e:
            print(f"❌ [routes/routes.py:get_history] Error getting history: {str(e)}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ [routes/routes.py:get_history] Unexpected error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/history/clear")
async def clear_history(request: SessionClearRequest):
    """Clear chat history for a session"""
    try:
        print(f"📥 [routes/routes.py:clear_history] Clearing history for session_id={request.session_id}")
        
        try:
            memory_store.clear_session(request.session_id)
            print(f"✅ [routes/routes.py:clear_history] Successfully cleared session")
            return {"status": "success", "message": f"History cleared for session {request.session_id}"}
        except Exception as e:
            print(f"❌ [routes/routes.py:clear_history] Error clearing history: {str(e)}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))
    except ValidationError as e:
        print(f"❌ [routes/routes.py:clear_history] Validation error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ [routes/routes.py:clear_history] Unexpected error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export/{session_id}")
async def export_session(session_id: str, filename: str = Query(default=None)):
    """Download a single session's chat history as a JSON file"""
    try:
        print(f"📥 [routes/routes.py:export_session] Exporting session_id={session_id}")
        history = memory_store.get_history(session_id)
        if not history:
            raise HTTPException(status_code=404, detail="Session not found or empty")

        export_payload = {"session_id": session_id, "messages": history}
        data = json.dumps(export_payload, ensure_ascii=False, indent=2)
        download_name = filename or f"chat_{session_id}.json"
        headers = {
            "Content-Disposition": f"attachment; filename=\"{download_name}\""
        }
        return Response(content=data, media_type="application/json", headers=headers)
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ [routes/routes.py:export_session] Unexpected error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export")
async def export_all(filename: str = Query(default="chats_export.json")):
    """Download all sessions' chat histories as a JSON file"""
    try:
        print("📥 [routes/routes.py:export_all] Exporting all sessions")
        all_histories = memory_store.get_all_histories()
        export_payload = {"sessions": all_histories}
        data = json.dumps(export_payload, ensure_ascii=False, indent=2)
        headers = {
            "Content-Disposition": f"attachment; filename=\"{filename}\""
        }
        return Response(content=data, media_type="application/json", headers=headers)
    except Exception as e:
        print(f"❌ [routes/routes.py:export_all] Unexpected error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
