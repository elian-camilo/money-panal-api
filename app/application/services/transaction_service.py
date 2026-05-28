from app.domain.entities.user import User
from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.transaction import Transaction
from app.domain.exceptions import (
    ResourceNotFoundException,  
    InvalidAmountException,
    UnauthorizedException,
)
from app.core.logger import get_logger

logger = get_logger(__name__)


class CreateTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, transaction: Transaction, user_id: int) -> Transaction:
        
        with self.uow:
            transaction_saved = self.uow.transaction_repository.save(transaction)

        logger.info("transaction_created", id=transaction_saved.id, amount=transaction_saved.amount, account=transaction_saved.account_id, user_id=transaction_saved.user_id)
        return transaction_saved
    
class ListTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int, current_user: User) -> list[Transaction]:
        with self.uow:
            transactions = self.uow.transaction_repository.get_all(offset, limit, user_id=current_user.id)

        logger.debug("transactions_listed", offset=offset, limit=limit, user_id=current_user.id)
        return transactions

class GetTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, current_user: User) -> Transaction:
        with self.uow:
            transaction = self.uow.transaction_repository.get_by_id(id)
            if not transaction:
                logger.warning("transaction_not_found", id=id)
                raise ResourceNotFoundException(f"Transaction ID:{id} doesn't exist.")
            if transaction.user_id != current_user.id:
                logger.warning("transaction_access_denied", id=id, user_id=current_user.id)
                raise UnauthorizedException(f"Access denied for Transaction ID:{id}.")

        logger.debug("transaction_retrieved", id=transaction.id)
        return transaction
    
class UpdateTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, transaction: Transaction, current_user: User) -> Transaction:
        with self.uow:
            # 1. Buscar la transacción real en la base de datos
            transaction_db = self.uow.transaction_repository.get_by_id(id)
            
            # 2. Validar existencia
            if not transaction_db:
                logger.warning("transaction_not_found", id=id)
                raise ResourceNotFoundException(f"Transaction ID:{id} doesn't exist.")
                
            # 3. Validar pertenencia (Ownership)
            if transaction_db.user_id != current_user.id:
                logger.warning("transaction_access_denied", id=id, user_id=current_user.id)
                raise UnauthorizedException(f"Access denied for Transaction ID:{id}.")

            # 4. Actualizar
            transaction_updated = self.uow.transaction_repository.update(id, transaction)
            
        logger.info("transaction_updated", id=transaction_updated.id, amount=transaction_updated.amount, account=transaction_updated.account_id, user_id=transaction_updated.user_id)
        return transaction_updated
    

class DeleteTransactionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, current_user: User) -> None:
        with self.uow:
            # 1. Buscar la transacción real en la base de datos
            transaction_db = self.uow.transaction_repository.get_by_id(id)
            
            # 2. Validar existencia
            if not transaction_db:
                logger.warning("transaction_not_found", id=id)
                raise ResourceNotFoundException(f"Transaction ID:{id} doesn't exist.")
                
            # 3. Validar pertenencia (Ownership)
            if transaction_db.user_id != current_user.id:
                logger.warning("transaction_access_denied", id=id, user_id=current_user.id)
                raise UnauthorizedException(f"Access denied for Transaction ID:{id}.")
            
            # 4. Eliminar
            self.uow.transaction_repository.delete(id)

        logger.info("transaction_deleted", id=id)