from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.account import Account
from app.domain.entities.user import User
from app.domain.exceptions import (
    ResourceNotFoundException,
    UnauthorizedException
)
from app.core.logger import get_logger

logger = get_logger(__name__)


class CreateAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, account: Account, user_id: int) -> Account:
        with self.uow:
            account_saved = self.uow.account_repository.save(account)

        logger.info("account_created", id=account_saved.id, name=account_saved.name, user_id=account_saved.user_id)
        return account_saved


class ListAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int, current_user: User) -> list[Account]:
        with self.uow:
            accounts_list = self.uow.account_repository.get_all(offset, limit, user_id=current_user.id)

        logger.debug("accounts_listed", offset=offset, limit=limit, user_id=current_user.id)
        return accounts_list


class GetAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, current_user: User) -> Account:
        with self.uow:
            account = self.uow.account_repository.get_by_id(id)
            if not account:
                logger.warning("account_not_found", id=id)
                raise ResourceNotFoundException(f"Account ID:{id} doesn't exist.")
            if account.user_id != current_user.id:
                logger.warning("account_access_denied", id=id, user_id=current_user.id)
                raise UnauthorizedException(f"Access denied for Account ID:{id}.")

        logger.debug("account_retrieved", id=account.id, name=account.name, user_id=account.user_id)
        return account


class UpdateAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, account: Account, current_user: User) -> Account:
        with self.uow:
            account_db = self.uow.account_repository.get_by_id(id)
            if not account_db:
                logger.warning("account_not_found", id=id)
                raise ResourceNotFoundException(f"Account ID:{id} doesn't exist.")
            if account_db.user_id != current_user.id:
                logger.warning("account_access_denied", id=id, user_id=current_user.id)
                raise UnauthorizedException(f"Access denied for Account ID:{id}.")

            account_updated = self.uow.account_repository.update(id, account)
            
        logger.info("account_updated", id=account_updated.id, name=account_updated.name, user_id=account_updated.user_id)
        return account_updated


class DeleteAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, current_user: User) -> None:
        with self.uow:
            account_db = self.uow.account_repository.get_by_id(id)
            if not account_db:
                logger.warning("account_not_found", id=id)
                raise ResourceNotFoundException(f"Account ID:{id} doesn't exist.")
            if account_db.user_id != current_user.id:
                logger.warning("account_access_denied", id=id, user_id=current_user.id)
                raise UnauthorizedException(f"Access denied for Account ID:{id}.")

            self.uow.account_repository.delete(id)
        logger.info("account_deleted", id=id)