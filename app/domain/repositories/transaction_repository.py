from abc import ABC, abstractmethod
from ..entities.transaction import Transaction

class TransactionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, transaction: Transaction) -> Transaction:
        pass

    @abstractmethod
    def get_all(self, offset: int, limit: int) -> list[Transaction]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Transaction:
        pass

    @abstractmethod
    def update(self, id: int, transaction: Transaction) -> Transaction:
        pass

    @abstractmethod
    def delete(self, id: int) -> dict:
        pass