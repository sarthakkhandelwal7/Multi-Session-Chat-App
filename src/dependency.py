from src.core import Settings
from fastapi import Request
from src.service import ChatService

def get_settings(request: Request) -> Settings:
    return request.app.state.settings

def get_chat_service(request: Request) -> ChatService:
    return request.app.state.chat_service