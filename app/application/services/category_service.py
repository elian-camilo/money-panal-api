from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.caterogy import Category
from app.domain.repositories.category_repository import CategoryRespositoryInterface

class CreateCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, category: Category) -> Category:
        # Business Rules
        if not category.name:
            raise ValueError("Category don't have a name.")
        
        return self.uow.category_repository.save(category)
    
class ListCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int) -> list[Category]:
        return self.uow.category_repository.get_all(offset, limit)
    
class GetCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> Category:
        category = self.uow.category_repository.get_by_id(id)
        if not category:
            raise ValueError("Category doesn't exist.")
        return category
    
class UpdateCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, category: Category) -> Category:
        category_updated = self.uow.category_repository.update(id, category)
        if not category_updated:
            raise ValueError("Category doesn't exist.")
        return category_updated
    
class DeleteCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> dict:
        category = self.uow.category_repository.delete(id)
        if not category:
            raise ValueError("Category doesn't exist.")
        return {
            "status": "success",
            "message": "Category deleted successfully",
            "delete_id": id
        }