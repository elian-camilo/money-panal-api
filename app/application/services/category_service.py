from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.caterogy import Category
from app.domain.exceptions import (
    ResourceNotFoundException,
    UnprocessableEntityException

)

class CreateCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, category: Category) -> Category:
        # Business Rules
        if not category.name:
            raise UnprocessableEntityException("Category don't have a name.")
        with self.uow:
            return self.uow.category_repository.save(category)
    
class ListCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int) -> list[Category]:
        with self.uow:
            return self.uow.category_repository.get_all(offset, limit)
    
class GetCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> Category:
        with self.uow:
            category = self.uow.category_repository.get_by_id(id)
            if not category:
                raise ResourceNotFoundException(f"Category ID:{id} doesn't exist.")
            return category
    
class UpdateCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, category: Category) -> Category:
        with self.uow:
            category_updated = self.uow.category_repository.update(id, category)
            if not category_updated:
                raise ResourceNotFoundException(f"Category ID:{id} doesn't exist.")
            return category_updated
    
class DeleteCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> dict:
        with self.uow:
            category = self.uow.category_repository.delete(id)
            if not category:
                raise ResourceNotFoundException(f"Category ID:{id} doesn't exist.")
            return {
                "status": "success",
                "message": "Category deleted successfully",
                "delete_id": id
            }