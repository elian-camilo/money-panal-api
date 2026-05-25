from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.debt import Debt
from app.domain.exceptions import (
    ResourceNotFoundException,
    UnprocessableEntityException,
)


class CreateDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, debt: Debt) -> Debt:
        if debt.amount < 0.0:
            raise UnprocessableEntityException("The amount don't be less than zero.")
        with self.uow:
            return self.uow.debt_repository.save(debt)

class ListDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int) -> list[Debt]:
        with self.uow:
            return self.uow.debt_repository.get_all(offset, limit)

class GetDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> Debt:
        with self.uow:
            debt = self.uow.debt_repository.get_by_id(id)
            if not debt:
                raise ResourceNotFoundException(f"Debt ID:{id} doesn't exist.")
            return debt

class UpdateDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, debt: Debt) -> Debt:
        with self.uow:
            debt_updated = self.uow.debt_repository.update(id, debt)
            if not debt_updated:
                raise ResourceNotFoundException(f"Debt ID:{id} doesn't exist.")
            return debt_updated

class DeleteDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id) -> dict:
        with self.uow:
            debt = self.uow.debt_repository.delete(id)
            if not debt:
                raise ResourceNotFoundException(f"Debt ID:{id} doesn't exist.")
            return {
                "status": "success",
                "message": "Debt deleted successfully",
                "delete_id": id
            }