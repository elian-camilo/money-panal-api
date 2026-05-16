from app.application.interfaces.unit_of_work import IUnitOfWork
from app.infraestructure.repositories.sqlmodel_transaction_repository import SQLModelTransactionRepository
from sqlmodel import Session

class UnitOfWork(IUnitOfWork):
    def __init__(self, session: Session):
        self.session = session

        self.transaction_repository = SQLModelTransactionRepository(self.session)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type: 
            self.session.rollback()
        else: 
            self.session.commit()