from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.user import User
from app.application.interfaces.password_hasher import PasswordHasherInterface
from app.application.interfaces.token_provider import ITokenProvider
from pydantic import BaseModel

class RegisterUserCommand(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class RegisterUserUseCase:
    def __init__(self, uow: IUnitOfWork, hasher: PasswordHasherInterface):
        self.uow = uow
        self.hasher = hasher

    def execute(self, command: RegisterUserCommand) -> User:
        hashed_password = self.hasher.hash_password(command.password)

        new_user = User(
            first_name=command.first_name,
            last_name=command.last_name,
            email=command.email,
            password=hashed_password
        )

        return self.uow.user_repository.save(new_user)

class LoginUserCommand(BaseModel):
    email: str
    password: str

class AuthenticateUserUseCase:
    def __init__(self, uow: IUnitOfWork, hasher: PasswordHasherInterface, token_provider: ITokenProvider):
        self.uow = uow
        self.hasher = hasher
        self.token_provider = token_provider

    def execute(self, command: LoginUserCommand) -> str:
        user = self.uow.user_repository.get_by_email(command.email)
        if not user:
            raise ValueError("Email or password incorrect.")

        is_valid = self.hasher.verify_password(command.password, user.password)
        if not is_valid:
            raise ValueError("Email or password incorrect.")

        payload = {"sub": user.email}
        return self.token_provider.generate_token(payload)

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