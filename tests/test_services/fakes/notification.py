from typing import Any

from src.interfaces.infrastructure.notifications import AbstractNotifications


class FakeNotifications(AbstractNotifications):
    def __init__(self):
        self.sent: dict = {}

    def send(self, destination: str, template: str, data: dict[str, Any]) -> None:
        self.sent[destination] = data
