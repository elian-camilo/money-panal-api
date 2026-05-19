from app.application.interfaces.unit_of_work import IUnitOfWork
from app.infraestructure.repositories.sqlmodel_transaction_repository import SQLModelTransactionRepository
from app.infraestructure.repositories.sqlmodel_category_repository import SQLModelCategoryRespository
from sqlmodel import Session

class UnitOfWork(IUnitOfWork):
    def __init__(self, session: Session):
        self.session = session

        self.transaction_repository = SQLModelTransactionRepository(self.session)
        self.category_repository = SQLModelCategoryRespository(self.session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type: 
            self.session.rollback()
        else: 
            self.session.commit()