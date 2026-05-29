from sqlmodel import Session, select
from app.domain.repositories.transaction_repository import TransactionRepositoryInterface
from app.domain.entities.transaction import Transaction as TransactionEntity
from ..models.transaction import TransactionTable


class SQLModelTransactionRepository(TransactionRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def save(self, transaction: TransactionEntity) -> TransactionEntity:
        data = transaction.model_dump(exclude_none=True)
        transaction_db = TransactionTable.model_validate(data)
        self.session.add(transaction_db)
        self.session.flush()
        self.session.refresh(transaction_db)

        return TransactionEntity.model_validate(transaction_db)
    
    def get_all(self, offset: int, limit: int, user_id: int) -> list[TransactionEntity]:
        transaction_db = self.session.exec(select(TransactionTable).where(TransactionTable.user_id==user_id).offset(offset).limit(limit)).all()
        return [TransactionEntity.model_validate(transaction) for transaction in transaction_db]
    
    def get_by_id(self, id: int):
        transaction_db = self.session.get(TransactionTable, id)
        if not transaction_db:
            return None
        return TransactionEntity.model_validate(transaction_db)
    
    def update(self, id: int, transaction: TransactionEntity) -> TransactionEntity:
        transaction_db = self.session.get(TransactionTable, id)
        if not transaction_db:
            return None
        
        # Exclude immutable/managed fields to prevent resetting or tampering
        data_transaction = transaction.model_dump(exclude={"id", "user_id", "created_at"})

        transaction_db.sqlmodel_update(data_transaction)

        self.session.add(transaction_db)
        self.session.flush()
        self.session.refresh(transaction_db)

        return TransactionEntity.model_validate(transaction_db)
    
    def delete(self, id: int) -> bool:
        transaction_db = self.session.get(TransactionTable, id)
        if not transaction_db:
            return None
        self.session.delete(transaction_db)
        self.session.flush()

        return True