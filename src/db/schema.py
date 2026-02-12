from sqlalchemy.ext.declarative import declarative_base
from src.core import Settings


from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    Integer,
    func,
    Date,
    Boolean,
    UUID,
    Index,
    text,
)

Base = declarative_base()

settings = Settings()


class User(Base):
    __tablename__ = "user"

    user_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    email = Column(String, unique=True, nullable=False)


class ChatSession(Base):
    __tablename__ = "chat_session"
    session_id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(String, foreign_key="user.user_id", nullable=False)
    title = Column(String, nullable=False, server_default="New Chat")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __tableargs__ = (
        Index("idx_user_updated_at", text("user_id, updated_at DESC")),
        {"schema": settings.active_schema},
    )


class ChatMessage(Base):
    __tablename__ = "chat_message"

    message_id = Column(String, primary_key=True)
    session_id = Column(String, foreign_key="")