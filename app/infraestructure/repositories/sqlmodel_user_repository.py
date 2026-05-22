from sqlmodel import Session, select
from app.domain.repositories.user_repository import UserRepositoryInterface
from app.domain.entities.user import User as UserEntity
from ..models.user import UserTable


class SQLModelUserRespository(UserRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: UserEntity) -> UserEntity:
        user_db = UserTable.model_validate(user)
        self.session.add(user_db)
        self.session.flush()
        self.session.refresh(user_db)
        return UserEntity.model_validate(user_db)
    
    def get_all(self, offset: int, limit: int) -> list[UserEntity]:
        user_db = self.session.exec(select(UserTable).offset(offset).limit(limit)).all()
        return [UserEntity.model_validate(user) for user in user_db]
    
    def get_by_id(self, id: int) -> UserEntity:
        user_db = self.session.get(UserTable, id)
        if not user_db:
            return None
        return UserEntity.model_validate(user_db)

    def get_by_email(self, email: str) -> UserEntity:
        user_db = self.session.exec(select(UserTable).where(UserTable.email == email)).first()
        if not user_db:
            return None
        return UserEntity.model_validate(user_db)
    
    def update(self, id: int, user: UserEntity) -> UserEntity:
        user_db = self.session.get(UserTable, id)
        if not user_db:
            return None
        user_data = user.model_dump()
        user_db.sqlmodel_update(user_data)
        self.session.add(user_db)
        self.session.flush()
        self.session.refresh(user_db)
        return UserEntity.model_validate(user_db)
    
    def delete(self, id: int) -> bool:
        user_db = self.session.get(UserTable, id)
        if not user_db:
            return None
        self.session.delete(user_db)
        self.session.flush()
        return True