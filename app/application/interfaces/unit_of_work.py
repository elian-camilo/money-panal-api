from abc import ABC, abstractmethod
from app.domain.repositories.transaction_repository import TransactionRepositoryInterface
from app.domain.repositories.category_repository import CategoryRespositoryInterface
from app.domain.repositories.account_repository import AccountRepositoryInterface
from app.domain.repositories.obligation_repository import ObligationRepositoryInterface
from app.domain.repositories.debt_repository import DebtRepositoryInterface


class IUnitOfWork(ABC):
    transaction_repository: TransactionRepositoryInterface
    category_repository: CategoryRespositoryInterface
    accout_repository: AccountRepositoryInterface
    obligation_repository: ObligationRepositoryInterface
    debt_repository: DebtRepositoryInterface

    @abstractmethod
    def __enter__(self): 
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb): 
        pass