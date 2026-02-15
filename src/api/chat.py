from fastapi import APIRouter, Depends, HTTPException
from src.dependency import get_chat_service
from src.service import ChatService
from src.schema import (
    NewChatSessionRequest,
    NewChatSessionResponse,
    ChatSessionResponse,
    ChatMessageResponse,
    SaveChatMessagesRequest,
)
from typing import List

chat_router = APIRouter(prefix="/chat", tags=["chat", "session"])


@chat_router.post(path="/session", response_model=NewChatSessionResponse)
async def create_new_session(
    new_chat_request: NewChatSessionRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> NewChatSessionResponse:
    """Create a new chat session"""
    return await chat_service.create_new_session(new_chat_request)


@chat_router.get(path="/session/{session_id}", response_model=ChatSessionResponse)
async def fetch_chat_session(
    session_id: str, chat_service: ChatService = Depends(get_chat_service)
) -> ChatSessionResponse:
    """Fetch a specific chat session by ID"""
    session = await chat_service.fetch_chat_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return ChatSessionResponse(**session)


@chat_router.get(path="/sessions/{user_id}", response_model=List[ChatSessionResponse])
async def fetch_all_sessions(
    user_id: str, chat_service: ChatService = Depends(get_chat_service)
) -> List[ChatSessionResponse]:
    """Fetch all chat sessions for a user"""
    sessions = await chat_service.fetch_all_sessions(user_id)
    return [ChatSessionResponse(**session) for session in sessions]


@chat_router.post(path="/messages")
async def save_chat_messages(
    request: SaveChatMessagesRequest,
    chat_service: ChatService = Depends(get_chat_service),
):
    """Save chat messages for a session"""
    return await chat_service.save_chat_messages(request.session_id, request.messages)


@chat_router.get(
    path="/messages/{session_id}", response_model=List[ChatMessageResponse]
)
async def fetch_chat_messages(
    session_id: str, chat_service: ChatService = Depends(get_chat_service)
) -> List[ChatMessageResponse]:
    """Fetch all messages for a chat session"""
    messages = await chat_service.fetch_chat_messages(session_id)
    return [ChatMessageResponse(**message) for message in messages]
