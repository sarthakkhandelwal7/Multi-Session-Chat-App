from pydantic import BaseModel, Field, EmailStr
from typing import List


class NewChatSessionRequest(BaseModel):
    user_id: str = Field(description="User ID")
    title: str = Field(default="New Chat", description="Session title")


class SaveChatMessagesRequest(BaseModel):
    session_id: str = Field(description="Session ID")
    messages: List[dict] = Field(description="List of chat messages")


class CreateUserRequest(BaseModel):
    first_name: str = Field(description="User first name")
    last_name: str = Field(description="User last name")
    email: EmailStr = Field(description="User email address")


class UpdateUserRequest(BaseModel):
    first_name: str = Field(default=None, description="User first name")
    last_name: str = Field(default=None, description="User last name")
    email: EmailStr = Field(default=None, description="User email address")
