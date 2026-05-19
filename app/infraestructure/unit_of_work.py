from app.application.interfaces.unit_of_work import IUnitOfWork
from app.infraestructure.repositories.sqlmodel_transaction_repository import SQLModelTransactionRepository
from app.infraestructure.repositories.sqlmodel_category_repository import SQLModelCategoryRespository
from app.infraestructure.repositories.sqlmodel_account_repository import SQLModelAccountRespository
from app.infraestructure.repositories.sqlmodel_obligation_repository import SQLModelObligationRepository
from sqlmodel import Session

class UnitOfWork(IUnitOfWork):
    def __init__(self, session: Session):
        self.session = session

        self.transaction_repository = SQLModelTransactionRepository(self.session)
        self.category_repository = SQLModelCategoryRespository(self.session)
        self.accout_repository = SQLModelAccountRespository(self.session)
        self.obligation_repository = SQLModelObligationRepository(self.session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type: 
            self.session.rollback()
        else: 
            self.session.commit()