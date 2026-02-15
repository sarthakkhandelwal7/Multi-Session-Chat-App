from pydantic import BaseModel, Field


class NewChatSessionResponse(BaseModel):
    session_id: str = Field(description="Session ID")
