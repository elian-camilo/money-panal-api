from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import TransactionRepositoryInterface

class CreateTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, transaction: Transaction) -> Transaction:
        # Business Rules
        if transaction.amount < 0:
            raise ValueError("The amount don't be less than zero.")
        
        # Pass to repository and save
        return self.uow.transaction_repository.save(transaction)