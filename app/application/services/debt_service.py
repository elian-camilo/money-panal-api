from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.debt import Debt
from app.domain.entities.user import User
from app.domain.exceptions import (
    ResourceNotFoundException,
    UnauthorizedException
)
from app.core.logger import get_logger

logger = get_logger(__name__)


class CreateDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, debt: Debt) -> Debt:
        with self.uow:
            debt_saved = self.uow.debt_repository.save(debt)

        logger.info("debt_created", id=debt_saved.id, amount=debt_saved.amount, due_date=debt_saved.due_date, user_id=debt_saved.user_id)
        return debt_saved


class ListDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int, current_user: User) -> list[Debt]:
        with self.uow:
            debts_list = self.uow.debt_repository.get_all(offset, limit, user_id=current_user.id)
            
        logger.debug("debts_listed", offset=offset, limit=limit, user_id=current_user.id)
        return debts_list


class GetDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, current_user: User) -> Debt:
        with self.uow:
            debt = self.uow.debt_repository.get_by_id(id)
            if not debt:
                logger.warning("debt_not_found", id=id)
                raise ResourceNotFoundException(f"Debt ID:{id} doesn't exist.")
            
            if debt.user_id != current_user.id:
                logger.warning("debt_unauthorized_access", id=id, user_id=current_user.id)
                raise UnauthorizedException("You don't have access to this resource.")
                
        logger.debug("debt_retrieved", id=debt.id, amount=debt.amount, due_date=debt.due_date, user_id=debt.user_id)
        return debt


class UpdateDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, debt: Debt, current_user: User) -> Debt:
        with self.uow:
            existing_debt = self.uow.debt_repository.get_by_id(id)
            if not existing_debt:
                logger.warning("debt_not_found", id=id)
                raise ResourceNotFoundException(f"Debt ID:{id} doesn't exist.")
                
            if existing_debt.user_id != current_user.id:
                logger.warning("debt_unauthorized_access", id=id, user_id=current_user.id)
                raise UnauthorizedException("You don't have access to this resource.")
                
            debt_updated = self.uow.debt_repository.update(id, debt)
            
        logger.debug("debt_updated", id=debt_updated.id, amount=debt_updated.amount, due_date=debt_updated.due_date, user_id=debt_updated.user_id)
        return debt_updated


class DeleteDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, current_user: User) -> None:
        with self.uow:
            existing_debt = self.uow.debt_repository.get_by_id(id)
            if not existing_debt:
                logger.warning("debt_not_found", id=id)
                raise ResourceNotFoundException(f"Debt ID:{id} doesn't exist.")
                
            if existing_debt.user_id != current_user.id:
                logger.warning("debt_unauthorized_access", id=id, user_id=current_user.id)
                raise UnauthorizedException("You don't have access to this resource.")
                
            self.uow.debt_repository.delete(id)

        logger.info("debt_deleted", id=id)