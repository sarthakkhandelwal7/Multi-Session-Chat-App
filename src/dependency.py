from src.core import Settings
from fastapi import Request

def get_settings(request: Request) -> Settings:
    return request.app.state.settings