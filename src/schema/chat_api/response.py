from pydantic import BaseModel, Field
from datetime import datetime


class NewChatSessionResponse(BaseModel):
    session_id: str = Field(description="Session ID")


class ChatSessionResponse(BaseModel):
    session_id: str = Field(description="Session ID")
    user_id: str = Field(description="User ID")
    title: str = Field(description="Session title")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class ChatMessageResponse(BaseModel):
    message_id: str = Field(description="Message ID")
    session_id: str = Field(description="Session ID")
    content: str = Field(description="Message content")
    role: str = Field(description="Message role (user/assistant)")
    created_at: datetime = Field(description="Creation timestamp")


class UserResponse(BaseModel):
    user_id: str = Field(description="User ID")
    first_name: str = Field(description="User first name")
    last_name: str = Field(description="User last name")
    email: str = Field(description="User email")
    created_at: datetime = Field(description="User creation timestamp")


class CreateUserResponse(BaseModel):
    user_id: str = Field(description="User ID")
