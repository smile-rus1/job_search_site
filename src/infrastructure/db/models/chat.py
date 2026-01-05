from __future__ import annotations
from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.db.models.base import Base
from src.infrastructure.enums_db import ChatTypeEnumDB, ActorTypeEnumDB


class ChatDB(Base):
    __tablename__ = "chats"

    chat_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_type: Mapped[ChatTypeEnumDB] = mapped_column(
        ChatTypeEnumDB, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    response_id: Mapped[int | None] = mapped_column(
        ForeignKey("responses.response_id", ondelete="CASCADE"), nullable=True
    )
    response: Mapped["ResponsesDB"] = relationship(back_populates="chat")  # type: ignore
    messages: Mapped[list["MessageDB"]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )


class MessageDB(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sender_type: Mapped[ActorTypeEnumDB] = mapped_column(ActorTypeEnumDB, nullable=False)
    message_text: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["UserDB"] = relationship(back_populates="messages")  # type: ignore

    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.chat_id", ondelete="CASCADE"),
        nullable=False
    )
    chat: Mapped["ChatDB"] = relationship(back_populates="messages")
