from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.user import User

class CreateUserUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, user: User) -> User:
        return self.uow.user_repository.save(user)

class ListUserUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int) -> list[User]:
        return self.uow.user_repository.get_all(offset, limit)

class GetUserUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> User:
        user = self.uow.user_repository.get_by_id(id)
        if not user:
            raise ValueError("User doesn't exist.")
        return user

class UpdateUserUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, user: User) -> User:
        user_updated = self.uow.user_repository.update(id, user)
        if not user_updated:
            return ValueError("User doesn't exist.")
        return user_updated

class DeleteUserUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> dict:
        user = self.uow.user_repository.delete(id)
        if not user:
            raise ValueError("User doesn't exist.")
        return {
            "status": "success",
            "message": "User deleted successfully",
            "delete_id": id
        }