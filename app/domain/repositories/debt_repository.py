from abc import ABC, abstractmethod
from ..entities.debt import Debt

class DebtRepositoryInterface(ABC):
    @abstractmethod
    def save(self, debt: Debt) -> Debt:
        pass

    @abstractmethod
    def get_all(self, offset: int, limit: int, user_id: int | None = None) -> list[Debt]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Debt:
        pass

    @abstractmethod
    def update(self, id: int, debt: Debt) -> Debt:
        pass

    @abstractmethod
    def delete(self, id: int) -> dict:
        pass