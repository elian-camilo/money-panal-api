from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.user import User
from app.application.interfaces.password_hasher import PasswordHasherInterface
from app.application.interfaces.token_provider import ITokenProvider
from pydantic import BaseModel
from app.domain.exceptions import (
    ResourceNotFoundException,
    UnauthorizedException,
)
from app.core.logger import get_logger

logger = get_logger(__name__)


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
        with self.uow:
            hashed_password = self.hasher.hash_password(command.password)

            new_user = User(
                first_name=command.first_name,
                last_name=command.last_name,
                email=command.email,
                password=hashed_password
            )

            user_saved = self.uow.user_repository.save(new_user)
        logger.info("user_created", name=user_saved.first_name, user_id=user_saved.id)
        return user_saved


class LoginUserCommand(BaseModel):
    email: str
    password: str


class AuthenticateUserUseCase:
    def __init__(self, uow: IUnitOfWork, hasher: PasswordHasherInterface, token_provider: ITokenProvider):
        self.uow = uow
        self.hasher = hasher
        self.token_provider = token_provider

    def execute(self, command: LoginUserCommand) -> str:
        with self.uow:
            user = self.uow.user_repository.get_by_email(command.email)
            if not user:
                logger.warning("invalid_credentials")
                raise UnauthorizedException("Email or password incorrect.")

            is_valid = self.hasher.verify_password(command.password, user.password)
            if not is_valid:
                logger.warning("invalid_credentials")
                raise UnauthorizedException("Email or password incorrect.")

            payload = {"sub": user.email}
            return self.token_provider.generate_token(payload)


class ListUserUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int, current_user: User) -> list[User]:
        """
        with self.uow:
            users = self.uow.user_repository.get_all(offset, limit)
        """
        # Regular users are not allowed to list all users
        logger.warning("unauthorized_user_list_attempt", user_id=current_user.id)
        raise UnauthorizedException("You don't have permission to list users.")


class GetUserUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, current_user: User) -> User:
        if id != current_user.id:
            logger.warning("unauthorized_user_access_attempt", target_id=id, user_id=current_user.id)
            raise UnauthorizedException("You don't have access to this resource.")

        with self.uow:
            user = self.uow.user_repository.get_by_id(id)
            if not user:
                logger.warning("user_not_found", id=id)
                raise ResourceNotFoundException(f"User ID:{id} doesn't exist.")
            
        logger.debug("user_retrieved", id=id)    
        return user


class UpdateUserUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, user: User, current_user: User) -> User:
        if id != current_user.id:
            logger.warning("unauthorized_user_update_attempt", target_id=id, user_id=current_user.id)
            raise UnauthorizedException("You don't have access to this resource.")

        with self.uow:
            existing_user = self.uow.user_repository.get_by_id(id)
            if not existing_user:
                logger.warning("user_not_found", id=id)
                raise ResourceNotFoundException(f"User ID:{id} doesn't exist.")

            user_updated = self.uow.user_repository.update(id, user)

        logger.info("user_updated", name=user_updated.first_name, user_id=user_updated.id)
        return user_updated


class DeleteUserUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, current_user: User) -> None:
        if id != current_user.id:
            logger.warning("unauthorized_user_delete_attempt", target_id=id, user_id=current_user.id)
            raise UnauthorizedException("You don't have access to this resource.")

        with self.uow:
            existing_user = self.uow.user_repository.get_by_id(id)
            if not existing_user:
                logger.warning("user_not_found", id=id)
                raise ResourceNotFoundException(f"User ID:{id} doesn't exist.")
                
            self.uow.user_repository.delete(id)

        logger.info("user_deleted", id=id)