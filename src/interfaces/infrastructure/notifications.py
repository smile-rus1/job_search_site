import abc
from typing import Any


class AbstractNotifications(abc.ABC):
    @abc.abstractmethod
    def send(self, destination: str, template: str, data: dict[str, Any]) -> None:
        raise NotImplementedError
