from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.account import Account
from app.domain.exceptions import (
    ResourceNotFoundException,  
    InvalidAmountException,
)


class CreateAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, account: Account) -> Account:
        if account.profit_percentage < 0.0:
            raise InvalidAmountException("The profit percentage don't be less than zero.")
        with self.uow:
            return self.uow.account_repository.save(account)

class ListAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int) -> list[Account]:
        with self.uow:
            return self.uow.account_repository.get_all(offset, limit)

class GetAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> Account:
        with self.uow:
            account = self.uow.account_repository.get_by_id(id)
            if not account:
                raise ResourceNotFoundException("Account ID:{id} doesn't exist.")
            return account

class UpdateAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, account: Account) -> Account:
        with self.uow:
            account_updated = self.uow.account_repository.update(id, account)
            if not account_updated:
                return ResourceNotFoundException("Account ID:{id} doesn't exist.")
            return account_updated

class DeleteAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> dict:
        with self.uow:
            account = self.uow.account_repository.delete(id)
            if not account:
                raise ResourceNotFoundException("Account ID:{id} doesn't exist.")
            return {
                "status": "success",
                "message": "Account deleted successfully",
                "delete_id": id
            }