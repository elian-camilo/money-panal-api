from abc import ABC, abstractmethod
from ..entities.user import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def get_all(self, offset: int, limit: int) -> list[User]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def update(self, id: int, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, id: int) -> dict:
        pass