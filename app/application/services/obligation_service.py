from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.obligation import Obligation
from datetime import date
from app.domain.exceptions import (
    ResourceNotFoundException,
    UnprocessableEntityException
)


class CreateObligationUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, obligation: Obligation) -> Obligation:
        # Business Rules
        if obligation.amount < 0.0:
            raise UnprocessableEntityException("The amount don't be less than zero.")
        if obligation.due_date < date.today():
            raise UnprocessableEntityException("The due date don't be less than today.")
        with self.uow:
            return self.uow.obligation_repository.save(obligation)
    
class ListObligationUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int) -> list[Obligation]:
        with self.uow:
            return self.uow.obligation_repository.get_all(offset, limit)
    
class GetObligationUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> Obligation:
        with self.uow:
            obligation = self.uow.obligation_repository.get_by_id(id)
            if not obligation:
                raise ResourceNotFoundException(f"Obligation ID:{id} doesn't exist.")
            return obligation
    
class UpdateObligationUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, obligation: Obligation) -> Obligation:
        with self.uow:
            obligation_updated = self.uow.obligation_repository.update(id, obligation)

            if obligation.due_date < date.today():
                raise UnprocessableEntityException("The due date don't be less than today.")

            if not obligation_updated:
                raise ResourceNotFoundException(f"Obligation ID:{id} doesn't exist.")
            return obligation_updated
    
class DeleteObligationUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> dict:
        with self.uow:
            obligation = self.uow.obligation_repository.delete(id)
            if not obligation:
                raise ResourceNotFoundException(f"Obligation ID:{id} doesn't exist.")
            return {
                "status": "success",
                "message": "Obligation deleted successfully",
                "delete_id": id
            } 