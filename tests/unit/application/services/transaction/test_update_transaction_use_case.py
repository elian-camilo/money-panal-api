import pytest
from unittest.mock import MagicMock

from app.application.services.transaction_service import UpdateTransactionUseCase
from app.domain.entities.transaction import Transaction
from app.domain.entities.user import User
from app.domain.exceptions import ResourceNotFoundException, UnauthorizedException

def test_update_transaction_success():
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
    uow.transaction_repository.get_by_id.return_value = fake_transaction

    use_case = UpdateTransactionUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    transaction_to_update = Transaction(
        amount=200.0,
        t_type="expense",
        description="Salary",
        category_id=2,
        account_id=2
    )
    transaction_updated = Transaction(
        id=1,
        amount=200.0,
        t_type="expense",
        description="Salary",
        category_id=2,
        account_id=2,
        user_id=1,
        created_at=None
    )

    uow.transaction_repository.update.return_value = transaction_updated

    result = use_case.execute(id=1, transaction=transaction_to_update, current_user=current_user)

    assert result.amount == 200
    assert result.t_type == "expense"
    assert result == transaction_updated

    uow.transaction_repository.get_by_id.assert_called_once_with(1)
    uow.transaction_repository.update.assert_called_once_with(1, transaction_to_update)


def test_update_transaction_not_found():
    uow = MagicMock()
    uow.transaction_repository.get_by_id.return_value = None

    use_case = UpdateTransactionUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    transaction_to_update = Transaction(
        amount=200.0,
        t_type="expense",
        description="Salary",
        category_id=2,
        account_id=2
    )

    with pytest.raises(ResourceNotFoundException) as exc_info:
        use_case.execute(id=999, transaction=transaction_to_update, current_user=current_user)

    assert str(exc_info.value) == "Transaction ID:999 doesn't exist."

    uow.transaction_repository.get_by_id.assert_called_once_with(999)
    uow.transaction_repository.update.assert_not_called()


def test_update_transaction_access_denied():
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
    uow.transaction_repository.get_by_id.return_value = fake_transaction

    use_case = UpdateTransactionUseCase(uow=uow)
    current_user = User(
        id=2,
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    transaction_to_update = Transaction(
        amount=200.0,
        t_type="expense",
        description="Salary",
        category_id=2,
        account_id=2
    )
    with pytest.raises(UnauthorizedException) as exc_info:
        use_case.execute(id=1, transaction=transaction_to_update, current_user=current_user)

    assert str(exc_info.value) == "Access denied for Transaction ID:1."

    uow.transaction_repository.get_by_id.assert_called_once_with(1)
    uow.transaction_repository.update.assert_not_called()