from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.account import Account

class CreateAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, account: Account) -> Account:
        if account.profit_percentage < 0.0:
            raise ValueError("The profit percentaje don't be less than zero.")
        
        return self.uow.accout_repository.save(account)

class ListAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int) -> list[Account]:
        return self.uow.accout_repository.get_all(offset, limit)

class GetAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> Account:
        account = self.uow.accout_repository.get_by_id(id)
        if not account:
            raise ValueError("Account doesn't exist.")
        return account

class UpdateAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, account: Account) -> Account:
        account_updated = self.uow.accout_repository.update(id, account)
        if not account_updated:
            return ValueError("Account doesn't exist.")
        return account_updated

class DeleteAccountUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int) -> dict:
        account = self.uow.accout_repository.delete(id)
        if not account:
            raise ValueError("Account doesn't exist.")
        return {
            "status": "success",
            "message": "Account deleted successfully",
            "delete_id": id
        }