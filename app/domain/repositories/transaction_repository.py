from abc import ABC, abstractmethod
from ..entities.transaction import Transaction

class TransactionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, transaction: Transaction) -> Transaction:
        pass