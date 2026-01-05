from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseChatException(BaseExceptions):
    ...


@dataclass
class ChatPermissionError(BaseChatException):
    chat_id: int

    def message(self):
        return f"You do not have permissions to chat {self.chat_id}"
