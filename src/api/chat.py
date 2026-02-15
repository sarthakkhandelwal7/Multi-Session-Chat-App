from fastapi import APIRouter, Depends, HTTPException
from src.dependency import get_chat_service
from src.service import ChatService
from src.schema import NewChatSessionRequest

chat_router = APIRouter(prefix="/chat", tags=["chat", "session"])


@chat_router.get(path="/session")
async def create_new_session(
    new_chat_request: NewChatSessionRequest,
    chat_service: ChatService = Depends(get_chat_service)
    ):
    session_id = chat_service.create_new_session(new_chat_request)
    return {"session_id": session_id}

@chat_router.get(path="/session/{session_id}")
async def fetch_chat_session(chat_service: ChatService = Depends(get_chat_service)):
    
