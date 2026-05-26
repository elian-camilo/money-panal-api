from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.transaction import Transaction
from app.domain.exceptions import (
    ResourceNotFoundException,  
    InvalidAmountException,
)
from app.core.logger import get_logger

logger = get_logger(__name__)


class CreateTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, transaction: Transaction) -> Transaction:
        with self.uow:
            transaction_saved = self.uow.transaction_repository.save(transaction)

        logger.info("transaction_created", id=transaction_saved.id, amount=transaction.amount, account=transaction.account_id, user_id=transaction.user_id)
        return transaction_saved
    
class ListTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int) -> list[Transaction]:
        with self.uow:
            transactions = self.uow.transaction_repository.get_all(offset, limit)

        logger.debug("transactions_listed", offset=offset, limit=limit)
        return transactions

class GetTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> Transaction:
        with self.uow:
            transaction = self.uow.transaction_repository.get_by_id(id)
            if not transaction:
                logger.warning("transaction_not_found", id=id)
                raise ResourceNotFoundException(f"Transaction ID:{id} doesn't exist.")

        logger.debug("transaction_retrieved", id=transaction.id)
        return transaction
    
class UpdateTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, transaction: Transaction) -> Transaction:
        with self.uow:
            transaction_updated = self.uow.transaction_repository.update(id, transaction)
            if not transaction_updated:
                logger.warning("transaction_not_found", id=id)
                raise ResourceNotFoundException(f"Transaction ID:{id} doesn't exist.")
            
        logger.info("transaction_updated", id=transaction_updated.id, amount=transaction.amount, account=transaction.account_id, user_id=transaction.user_id)
        return transaction_updated
    

class DeleteTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> None:
        with self.uow:
            transaction = self.uow.transaction_repository.delete(id)
            if not transaction:
                logger.warning("transaction_not_found", id=id)
                raise ResourceNotFoundException(f"Transaction ID:{id} doesn't exist.")

        logger.info("transaction_deleted", id=id)