from sqlmodel import Session
from app.domain.repositories.transaction_repository import TransactionRepositoryInterface
from app.domain.entities.transaction import Transaction as TransactionEntity
from ..models.transaction import TransactionTable


class SQLModelTransactionRepository(TransactionRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def save(self, transaction: TransactionEntity) -> TransactionEntity:
        transaction_db = TransactionTable.model_validate(transaction)

        # Physical actions on DB
        self.session.add(transaction_db)
        self.session.commit()
        self.session.refresh(transaction_db)

        return TransactionEntity.model_validate(transaction_db)