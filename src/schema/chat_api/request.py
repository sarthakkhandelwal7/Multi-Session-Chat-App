from pydantic import BaseModel, Field

class NewChatSessionRequest(BaseModel):
    user_id: str = Field(description="User ID")
    title: str = Field(default="New Chat", description="Session title")