from abc import ABC, abstractmethod
from ..entities.obligation import Obligation

class ObligationRepositoryInterface(ABC):
    @abstractmethod
    def save(self, obligation: Obligation) -> Obligation:
        pass

    @abstractmethod
    def get_all(self, offset: int, limit: int, user_id: int) -> list[Obligation]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Obligation:
        pass

    @abstractmethod
    def update(self, id: int, obligation: Obligation) -> Obligation:
        pass

    @abstractmethod
    def delete(self, id: int) -> dict:
        pass