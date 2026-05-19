from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.transaction import Transaction


class CreateTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, transaction: Transaction) -> Transaction:
        # Business Rules
        if transaction.amount < 0.0:
            raise ValueError("The amount don't be less than zero.")
        
        # Pass to repository and save
        return self.uow.transaction_repository.save(transaction)
    
class ListTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int) -> list[Transaction]:
        return self.uow.transaction_repository.get_all(offset, limit)
    
class GetTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> Transaction:
        transaction = self.uow.transaction_repository.get_by_id(id)
        if not transaction:
            raise ValueError("Transaction doesn't exist.")
        return transaction
    
class UpdateTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, transaction: Transaction) -> Transaction:
        transaction_uptated = self.uow.transaction_repository.update(id, transaction)
        if not transaction_uptated:
            raise ValueError("Transaction doesn't exist.")
        return transaction_uptated
    

class DeleteTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> dict:
        transaction = self.uow.transaction_repository.delete(id)
        if not transaction:
            raise ValueError("Transaction doesn't exist.")
        return {
            "status": "success",
            "message": "Transaction deleted successfully",
            "delete_id": id
        }