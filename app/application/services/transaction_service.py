from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.transaction import Transaction
from app.domain.exceptions import (
    ResourceNotFoundException,  
    InvalidAmountException,
)


class CreateTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, transaction: Transaction) -> Transaction:
        # Business Rules
        if transaction.amount < 0.0:
            raise InvalidAmountException("The amount don't be less than zero.")
        with self.uow:
            # Pass to repository and save
            return self.uow.transaction_repository.save(transaction)
    
class ListTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int) -> list[Transaction]:
        with self.uow:
            return self.uow.transaction_repository.get_all(offset, limit)
    
class GetTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> Transaction:
        with self.uow:
            transaction = self.uow.transaction_repository.get_by_id(id)
            if not transaction:
                raise ResourceNotFoundException(f"Transaction ID:{id} doesn't exist.")
            return transaction
    
class UpdateTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, transaction: Transaction) -> Transaction:
        with self.uow:
            transaction_uptated = self.uow.transaction_repository.update(id, transaction)
            if not transaction_uptated:
                raise ResourceNotFoundException(f"Transaction ID:{id} doesn't exist.")
            return transaction_uptated
    

class DeleteTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> dict:
        with self.uow:
            transaction = self.uow.transaction_repository.delete(id)
            if not transaction:
                raise ResourceNotFoundException(f"Transaction ID:{id} doesn't exist.")
            return {
                "status": "success",
                "message": "Transaction deleted successfully",
                "delete_id": id
            }