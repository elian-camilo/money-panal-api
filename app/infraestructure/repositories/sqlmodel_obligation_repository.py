from sqlmodel import Session, select
from app.domain.repositories.obligation_repository import ObligationRepositoryInterface
from app.domain.entities.obligation import Obligation as ObligationEntity
from ..models.obligation import ObligationTable

class SQLModelObligationRepository(ObligationRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def save(self, obligation: ObligationEntity) -> ObligationEntity:
        obligation_db = ObligationTable.model_validate(obligation)
        self.session.add(obligation_db)
        self.session.flush()
        self.session.refresh(obligation_db)
        return ObligationEntity.model_validate(obligation_db)
    
    def get_all(self, offset: int, limit: int) -> list[ObligationEntity]:
        obligation_db = self.session.exec(select(ObligationTable).offset(offset).limit(limit)).all()
        return [ObligationEntity.model_validate(obligation) for obligation in obligation_db]
    
    def get_by_id(self, id: int) -> ObligationEntity:
        obligation_db = self.session.get(ObligationTable, id)
        if not obligation_db:
            return None
        return ObligationEntity.model_validate(obligation_db)
    
    def update(self, id: int, obligation: ObligationEntity) -> ObligationEntity:
        obligation_db = self.session.get(ObligationTable, id)
        if not obligation_db:
            return None
        obligation_data = obligation.model_dump()
        obligation_db.sqlmodel_update(obligation_data)
        self.session.add(obligation_db)
        self.session.flush()
        self.session.refresh(obligation_db)
        return ObligationEntity.model_validate(obligation_db)
    
    def delete(self, id: int) -> bool:
        obligation_db = self.session.get(ObligationTable, id)
        if not obligation_db:
            return None
        self.session.delete(obligation_db)
        self.session.flush()
        return True