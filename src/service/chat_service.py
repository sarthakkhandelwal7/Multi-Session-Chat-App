from src.db.db_adapter import DatabaseAdapter
from src.core import Settings
from src.schema import NewChatSessionRequest, NewChatSessionResponse
from src.db.schema import ChatSession, ChatMessage
import logging


class ChatService:
    def __init__(self, db: DatabaseAdapter, settings: Settings):
        self.db = db
        self.settings = settings

    async def create_new_session(
        self, request: NewChatSessionRequest
    ) -> NewChatSessionResponse:
        try:
            response = await self.db.insert_rows(
                table_model=ChatSession,
                query_type="Create New chat session",
                rows=[request.model_dump()],
                returning=[ChatSession.session_id],
            )

            return NewChatSessionResponse(session_id=str(response[0]["session_id"]))

        except Exception as e:
            logging.error(f"Error creating new session: {e}")
            raise e

    async def fetch_chat_session(self, session_id: str):
        from sqlalchemy import select

        query = select(ChatSession).where(ChatSession.session_id == session_id)
        result = await self.db.execute_query(query)

        if not result:
            return None
        return result[0]

    async def fetch_all_sessions(self, user_id: str):
        from sqlalchemy import select

        query = (
            select(ChatSession)
            .where(ChatSession.user_id == user_id)
            .order_by(ChatSession.updated_at.desc())
        )
        return await self.db.execute_query(query)

    async def save_chat_messages(self, session_id: str, messages: list[dict]):
        try:
            response = await self.db.insert_rows(
                table_model=ChatMessage,
                query_type="Save chat messages",
                rows=messages,
                returning=[ChatMessage.message_id],
            )
            return response
        except Exception as e:
            logging.error(f"Error saving chat messages: {e}")
            raise e

    async def fetch_chat_messages(self, session_id: str):
        from sqlalchemy import select

        query = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
        )
        return await self.db.execute_query(query)
