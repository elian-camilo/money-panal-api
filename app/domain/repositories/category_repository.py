from abc import ABC, abstractmethod
from ..entities.caterogy import Category

class CategoryRespositoryInterface(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    def get_all(self, offset: int, limit: int) -> list[Category]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Category:
        pass

    @abstractmethod
    def update(self, id: int, category: Category) -> Category:
        pass

    @abstractmethod
    def delete(self, id: int) -> dict:
        pass