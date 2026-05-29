from sqlmodel import Session, select
from app.domain.repositories.account_repository import AccountRepositoryInterface
from app.domain.entities.account import Account as AccountEntity
from ..models.account import AccountTable


class SQLModelAccountRespository(AccountRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def save(self, account: AccountEntity) -> AccountEntity:
        data = account.model_dump(exclude_none=True)
        account_db = AccountTable.model_validate(data)
        self.session.add(account_db)
        self.session.flush()
        self.session.refresh(account_db)
        return AccountEntity.model_validate(account_db)
    
    def get_all(self, offset: int, limit: int, user_id: int) -> list[AccountEntity]:
        account_db = self.session.exec(select(AccountTable).where(AccountTable.user_id == user_id).offset(offset).limit(limit)).all()
        return [AccountEntity.model_validate(account) for account in account_db]
    
    def get_by_id(self, id: int) -> AccountEntity:
        account_db = self.session.get(AccountTable, id)
        if not account_db:
            return None
        return AccountEntity.model_validate(account_db)
    
    def update(self, id: int, account: AccountEntity) -> AccountEntity:
        account_db = self.session.get(AccountTable, id)
        if not account_db:
            return None
        account_data = account.model_dump(exclude_none=True, exclude={"id", "created_at", "user_id"})
        account_db.sqlmodel_update(account_data)
        self.session.add(account_db)
        self.session.flush()
        self.session.refresh(account_db)
        return AccountEntity.model_validate(account_db)
    
    def delete(self, id: int) -> bool:
        account_db = self.session.get(AccountTable, id)
        if not account_db:
            return None
        self.session.delete(account_db)
        self.session.flush()
        return True