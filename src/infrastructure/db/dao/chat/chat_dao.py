import datetime

from loguru import logger
from sqlalchemy import insert, select, or_, delete, update
from sqlalchemy.exc import IntegrityError

from src.dto.db.chat.chat import BaseChatDTODAO
from src.exceptions.infrascructure.chat.chat import BaseChatException, ChatPermissionError
from src.infrastructure.db.models import ChatDB, MessageDB, ResponsesDB, ResumeDB, VacancyDB
from src.interfaces.infrastructure.dao.chat_dao import IChatDAO
from src.interfaces.infrastructure.sqlalchemy_dao import SqlAlchemyDAO


class ChatDAO(SqlAlchemyDAO, IChatDAO):
    async def send_message(self, chat: BaseChatDTODAO) -> BaseChatDTODAO:
        sql_chat = (
            insert(MessageDB)
            .values(
                sender_type=chat.message.sender_type,
                message_text=chat.message.message_text,
                sender_id=chat.message.user.user_id,
                chat_id=chat.chat_id,
            )
            .returning(MessageDB.message_id)
        )

        try:
            res = await self._session.execute(sql_chat)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{BaseChatDTODAO.__name__} in {self.send_message.__name__}"
            ).error(f"WITH DATA {chat} IN SEND MESSAGE IN CHAT {chat.chat_id}\nMESSAGE: {exc}")
            raise self._error_parser(chat, exc)

        message_id = res.scalar()
        if message_id is None:
            raise ChatPermissionError(chat_id=chat.chat_id)

        chat.message.message_id = message_id
        chat.message.created_at = datetime.datetime.now()
        return chat

    async def change_message(self, chat: BaseChatDTODAO) -> None:
        sql = (  # что-то в SQL запросе не то
            update(MessageDB)
            .where(
                MessageDB.message_id == chat.message.message_id,
                MessageDB.sender_id == chat.message.user.user_id,
                MessageDB.chat_id == chat.chat_id
            )
            .values(message_text=chat.message.message_text)
        )
        try:
            await self._session.execute(sql)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{BaseChatDTODAO.__name__} in {self.change_message.__name__}"
            ).error(f"WITH DATA {chat} IN SEND MESSAGE IN CHAT {chat.chat_id}\nMESSAGE: {exc}")
            raise self._error_parser(chat, exc)

    async def delete_message(self, user_id: int, message_id: int, chat_id: int):
        sql = (
            delete(MessageDB)
            .where(
                MessageDB.message_id == message_id,
                MessageDB.sender_id == user_id,
                MessageDB.chat_id == chat_id
            )
        )
        res = await self._session.execute(sql)

        if res.rowcount == 0:
            raise ChatPermissionError(chat_id)

    async def user_have_permissions_in_chat(self, user_id: int, chat_id: int) -> bool:
        sql = (
            select(ChatDB.chat_id)
            .join(ResponsesDB, ResponsesDB.response_id == ChatDB.response_id)
            .outerjoin(ResumeDB, ResponsesDB.resume_id == ResumeDB.resume_id)
            .outerjoin(VacancyDB, ResponsesDB.resume_id == VacancyDB.vacancy_id)
            .where(ChatDB.chat_id == chat_id)
            .where(
                or_(
                    ResumeDB.applicant_id == user_id,
                    VacancyDB.company_id == user_id
                )
            )
        )
        res = (await self._session.execute(sql)).scalar_one_or_none()
        return res is not None

    @staticmethod
    def _error_parser(
            chat: BaseChatDTODAO,
            exc: IntegrityError
    ) -> BaseChatException:

        return BaseChatException()
