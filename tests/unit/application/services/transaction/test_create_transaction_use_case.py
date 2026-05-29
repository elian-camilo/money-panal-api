import pytest
from unittest.mock import MagicMock

from app.application.services.transaction_service import CreateTransactionUseCase
from app.domain.entities.transaction import Transaction

def test_create_transaction_success():
    uow = MagicMock()

    fake_transaction = Transaction(
        id=1,
        amount=100.0,
        t_type="income",
        description="Salary",
        category_id=1,
        account_id=1,
        user_id=1,
        created_at=None
    )

    uow.transaction_repository.save.return_value = fake_transaction

    use_case = CreateTransactionUseCase(uow=uow)
    transaction_to_create = Transaction(
        amount=100.0,
        t_type="income",
        description="Salary",
        category_id=1,
        account_id=1,
        user_id=1
    )
    result = use_case.execute(transaction_to_create, user_id=1)

    assert result.id == 1
    assert result == fake_transaction

    uow.transaction_repository.save.assert_called_once_with(transaction_to_create)