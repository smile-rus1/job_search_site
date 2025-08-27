from typing import Protocol


class IBaseTransactionManager(Protocol):
    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError
