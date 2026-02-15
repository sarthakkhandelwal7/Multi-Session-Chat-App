from src.db.db_adapter import DBAdapter
from src.core import Settings
from src.schema import NewChatSessionRequest, NewChatSessionResponse
from sqlalchemy import insert
from src.db.schema import User, ChatSession, ChatMessage
import uuid
import logging


class ChatService:
    def __init__(self, db: DBAdapter, settings: Settings):
        self.db = db
        self.settings = settings

    async def create_new_session(
        self, request: NewChatSessionRequest
    ) -> NewChatSessionResponse:
        try:
            response = self.db.insert_rows(
                table_model=ChatSession,
                query_type="Create New chat session",
                rows=[request.model_dump()],
                returning=ChatSession.session_id,
            )

            return NewChatSessionResponse(session_id=response[0]["session_id"])

        except Exception as e:
            logging.error(e)

    def fetch_chat_session(self, session_id):
        pass

    def fetch_all_sessions(self, user_id):
        pass

    def save_chat_messages(self, session_id, messages):
        pass
