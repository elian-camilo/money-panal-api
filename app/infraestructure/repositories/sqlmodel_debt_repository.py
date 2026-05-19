from sqlmodel import Session, select
from app.domain.repositories.debt_repository import DebtRepositoryInterface
from app.domain.entities.debt import Debt as DebtEntity
from ..models.debt import DebtTable


class SQLModelDebtRepository(DebtRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def save(self, debt: DebtEntity) -> DebtEntity:
        debt_db = DebtTable.model_validate(debt)
        self.session.add(debt_db)
        self.session.flush()
        self.session.refresh(debt_db)
        return DebtEntity.model_validate(debt_db)

    def get_all(self, offset: int, limit: int) -> list[DebtEntity]:
        debt_db = self.session.exec(select(DebtTable).offset(offset).limit(limit)).all()
        return [DebtEntity.model_validate(debt) for debt in debt_db]

    def get_by_id(self, id: int) -> DebtEntity:
        debt_db = self.session.get(DebtTable, id)
        if not debt_db:
            return None
        return DebtEntity.model_validate(debt_db)

    def update(self, id: int, debt: DebtEntity) -> DebtEntity:
        debt_db = self.session.get(DebtTable, id)
        if not debt_db:
            return None
        debt_data = debt.model_dump()
        debt_db.sqlmodel_update(debt_data)
        self.session.flush()
        self.session.refresh(debt_db)
        return DebtEntity.model_validate(debt_db)

    def delete(self, id: int) -> bool:
        debt_db = self.session.get(DebtTable, id)
        if not debt_db:
            return None
        self.session.delete(debt_db)
        self.session.flush()
        return True