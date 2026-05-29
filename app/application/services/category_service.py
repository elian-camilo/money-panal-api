from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.caterogy import Category
from app.domain.entities.user import User
from app.domain.exceptions import (
    ResourceNotFoundException,
    UnauthorizedException
)
from app.core.logger import get_logger

logger = get_logger(__name__)

class CreateCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, category: Category, user_id: int) -> Category:
        with self.uow:
            category_saved = self.uow.category_repository.save(category)

        logger.info("category_created", id=category_saved.id, name=category_saved.name, user_id=category_saved.user_id)
        return category_saved

class ListCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int, current_user: User) -> list[Category]:
        with self.uow:
            category_list = self.uow.category_repository.get_all(offset, limit, user_id=current_user.id)
            
        logger.debug("categories_listed", offset=offset, limit=limit, user_id=current_user.id)
        return category_list
    
class GetCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, current_user: User) -> Category:
        with self.uow:
            category = self.uow.category_repository.get_by_id(id)
            if not category:
                logger.warning("category_not_found", id=id)
                raise ResourceNotFoundException(f"Category ID:{id} doesn't exist.")
            if category.user_id != current_user.id:
                logger.warning("category_access_denied", id=id, user_id=current_user.id)
                raise UnauthorizedException(f"Access denied for Category ID:{id}.")
        logger.info("category_retrieved", id=category.id, name=category.name, user_id=category.user_id)
        return category
    
class UpdateCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, category: Category, current_user: User) -> Category:
        with self.uow:
            category_db = self.uow.category_repository.get_by_id(id)
            if not category_db:
                logger.warning("category_not_found", id=id)
                raise ResourceNotFoundException(f"Category ID:{id} doesn't exist.")
            if category_db.user_id != current_user.id:
                logger.warning("category_access_denied", id=id, user_id=current_user.id)
                raise UnauthorizedException(f"Access denied for Category ID:{id}.")

            category_updated = self.uow.category_repository.update(id, category)
            
        logger.info("category_updated", id=category_updated.id, name=category_updated.name, user_id=category_updated.user_id)
        return category_updated
    
class DeleteCategoryUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, current_user: User) -> None:
        with self.uow:
            category_db = self.uow.category_repository.get_by_id(id)
            if not category_db:
                logger.warning("category_not_found", id=id)
                raise ResourceNotFoundException(f"Category ID:{id} doesn't exist.")
            if category_db.user_id != current_user.id:
                logger.warning("category_access_denied", id=id, user_id=current_user.id)
                raise UnauthorizedException(f"Access denied for Category ID:{id}.")
                
            self.uow.category_repository.delete(id)
        logger.info("category_deleted", id=id)