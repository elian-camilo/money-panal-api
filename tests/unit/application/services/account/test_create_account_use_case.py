import pytest
from unittest.mock import MagicMock

from app.application.services.account_service import CreateAccountUseCase
from app.domain.entities.account import Account

def test_create_account_success():
    uow = MagicMock()

    fake_account = Account(
        id=1,
        name="Debit Card",
        amount=500.0,
        profit_percentage=1.5,
        currency="cop",
        user_id=1,
        created_at=None
    )

    uow.account_repository.save.return_value = fake_account

    use_case = CreateAccountUseCase(uow=uow)
    account_to_create = Account(
        name="Debit Card",
        amount=500.0,
        profit_percentage=1.5,
        currency="cop",
        user_id=1
    )
    result = use_case.execute(account_to_create, user_id=1)

    assert result.id == 1
    assert result == fake_account

    uow.account_repository.save.assert_called_once_with(account_to_create)
