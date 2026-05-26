from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.debt import Debt
from app.domain.exceptions import (
    ResourceNotFoundException,
    UnprocessableEntityException,
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

    def execute(self, offset: int, limit: int) -> list[Debt]:
        with self.uow:
            debts_list = self.uow.debt_repository.get_all(offset, limit)
            
        logger.debug("debts_listed", offset=offset, limit=limit)
        return debts_list

class GetDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> Debt:
        with self.uow:
            debt = self.uow.debt_repository.get_by_id(id)
            if not debt:
                logger.warning("debt_not_found", id=id)
                raise ResourceNotFoundException(f"Debt ID:{id} doesn't exist.")
                
        logger.debug("debt_retrieved", id=debt.id, amount=debt.amount, due_date=debt.due_date, user_id=debt.user_id)
        return debt

class UpdateDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, debt: Debt) -> Debt:
        with self.uow:
            debt_updated = self.uow.debt_repository.update(id, debt)
            if not debt_updated:
                logger.warning("debt_not_found", id=id)
                raise ResourceNotFoundException(f"Debt ID:{id} doesn't exist.")
            
        logger.debug("debt_retrieved", id=debt_updated.id, amount=debt_updated.amount, due_date=debt_updated.due_date, user_id=debt_updated.user_id)
        return debt_updated

class DeleteDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id) -> None:
        with self.uow:
            debt = self.uow.debt_repository.delete(id)
            if not debt:
                logger.warning("debt_not_found", id=id)
                raise ResourceNotFoundException(f"Debt ID:{id} doesn't exist.")

        logger.info("debt_deleted", id=id)