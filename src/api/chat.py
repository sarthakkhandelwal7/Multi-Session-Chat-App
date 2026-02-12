from fastapi import APIRouter, Depends, HTTPException
import uuid

chat_router = APIRouter(prefix="/chat", tags=["chat", "session"])


@chat_router.get(path="/session")
async def get_session():
    session_id = str(uuid.uuid4())
    return {"session_id": session_id}

