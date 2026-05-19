from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.debt import Debt


class CreateDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, debt: Debt) -> Debt:
        if debt.amount < 0.0:
            raise ValueError("The amount don't be less than zero.")
        return self.uow.debt_repository.save(debt)

class ListDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int) -> list[Debt]:
        return self.uow.debt_repository.get_all(offset, limit)

class GetDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> Debt:
        debt = self.uow.debt_repository.get_by_id(id)
        if not debt:
            raise ValueError("Debt doesn't exist.")
        return debt

class UpdateDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, debt: Debt) -> Debt:
        debt_updated = self.uow.debt_repository.update(id, debt)
        if not debt_updated:
            raise ValueError("Debt doesn't exist.")
        return debt_updated

class DeleteDebtUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id) -> dict:
        debt = self.uow.debt_repository.delete(id)
        if not debt:
            raise ValueError("Debt doesn't exist.")
        return {
            "status": "success",
            "message": "Debt deleted successfully",
            "delete_id": id
        }