from src.dto.web.auth import ActiveUser, AnonymousUser
from src.services.chat.chat import ChatService
from src.core.enums import ActorType
from src.dto.services.chat.chat import CreateMessageInChatDTO, ChangeMessageDTO
from src.dto.services.chat.message import CreateMessage


async def handle_send_message(
        data: dict,
        user: ActiveUser | AnonymousUser,
        chat_service: ChatService
):
    sender_type = None
    if user.type == "applicant":
        sender_type = ActorType.APPLICANT
    elif user.type == "company":
        sender_type = ActorType.COMPANY

    dto = CreateMessageInChatDTO(
        chat_id=data.get("chat_id"),
        create_message=CreateMessage(
            user_id=user.user_id,
            sender_type=sender_type,
            message_text=data.get("message")
        )
    )
    res = await chat_service.send_message(dto)
    return {
        "": ""
    }


async def handler_change_message(
        data: dict,
        user: ActiveUser | AnonymousUser,
        chat_service: ChatService
):
    dto = ChangeMessageDTO(
        chat_id=data.get("chat_id"),
        message_id=data.get("message_id"),
        user_id=user.user_id,
        message_text=data.get("message")
    )
    await chat_service.change_message(dto)

    return {
        "type": "change_message",
        "message_id": data.get("message_id")
    }


async def handler_delete_message_from_chat(
        data: dict,
        user: ActiveUser | AnonymousUser,
        chat_service: ChatService
):
    await chat_service.delete_message(
        user.user_id,
        data.get("message_id"),
        data.get("chat_id")
    )

    return {
        "type": "message_deleted",
        "message_id": data.get("message_id")
    }


handlers = {
    "send_message": handle_send_message,
    "change_message": handler_change_message,
    "delete_message": handler_delete_message_from_chat
}
