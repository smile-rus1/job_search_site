from src.interfaces.services.transaction_manager import IBaseTransactionManager
from test_services.fakes.dao_applicant import FakeApplicantDAO
from test_services.fakes.dao_company import FakeCompanyDAO
from test_services.fakes.redis_db import FakeRedisDB


class FakeTransactionalManager(IBaseTransactionManager):
    def __init__(self):
        self.committed = False

        self.applicant_dao = FakeApplicantDAO()
        self.company_dao = FakeCompanyDAO()
        self.redis_db = FakeRedisDB(dict())

    async def commit(self):
        self.committed = True

    async def rollback(self):
        pass
