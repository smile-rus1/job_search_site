from typing import Protocol, Any


class IDAO(Protocol):
    def create(self, data: Any) -> Any:
        raise NotImplementedError

    def delete(self, data: Any) -> Any | None:
        raise NotImplementedError
