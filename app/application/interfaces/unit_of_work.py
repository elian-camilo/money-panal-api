from abc import ABC, abstractmethod
from app.domain.repositories.transaction_repository import TransactionRepositoryInterface

class IUnitOfWork(ABC):
    transaction_repository: TransactionRepositoryInterface

    @abstractmethod
    def __enter__(self): pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb): pass