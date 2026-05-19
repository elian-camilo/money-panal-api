from abc import ABC, abstractmethod
from ..entities.account import Account

class AccountRepositoryInterface(ABC):
    @abstractmethod
    def save(self, account: Account) -> Account:
        pass

    @abstractmethod
    def get_all(self, offset: int, limit: int) -> list[Account]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Account:
        pass

    @abstractmethod
    def update(self, id: int, account: Account) -> Account:
        pass

    @abstractmethod
    def delete(self, id: int) -> dict:
        pass