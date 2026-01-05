from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from loguru import logger

from src.api.permissions import ws_login_required
from src.api.providers.abstract.services import chat_service_provider
from src.api.websockets.chat.handlers import handlers
from src.services.chat.chat import ChatService


chat_ws = APIRouter(
    prefix="/ws/chat",
    tags=["Chat"]
)


@chat_ws.websocket("/{chat_id}")
@ws_login_required
async def chat_ws_handler(
        ws: WebSocket,
        chat_id: int,
        chat_service: ChatService = Depends(chat_service_provider)
):
    await ws.accept()
    user = ws.scope["state"]  # тут работает всё, т.е из токена принимается user и потом просто идет проверка

    # проверка идет, что пользователь действительно состоит в этом чате
    if not await chat_service.user_have_permissions_in_chat(user.user_id, chat_id):
        await ws.close(code=1008, reason="Access denied")
        return

    try:
        while True:
            data = await ws.receive_json()
            data["chat_id"] = chat_id

            handler = handlers.get(data["type"])
            res = await handler(data, user, chat_service)

            await ws.send_json(res)

    except WebSocketDisconnect:
        ...

    except Exception as exc:
        logger.bind(
            app_name=f"{chat_ws_handler.__name__}"
        ).error(f"EXCEPTION IN WS-CHAT\nMESSAGE: {exc}")
        await ws.close(1011)
