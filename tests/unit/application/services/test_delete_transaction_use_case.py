import pytest
from unittest.mock import MagicMock

from app.application.services.transaction_service import DeleteTransactionUseCase
from app.domain.entities.transaction import Transaction
from app.domain.entities.user import User
from app.domain.exceptions import ResourceNotFoundException, UnauthorizedException

def test_delete_transaction_success():
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
    uow.transaction_repository.delete.return_value = True

    use_case = DeleteTransactionUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    use_case.execute(id=1, current_user=current_user)

    uow.transaction_repository.get_by_id.assert_called_once_with(1)
    uow.transaction_repository.delete.assert_called_once_with(1)

def test_delete_transaction_not_found():
    uow = MagicMock()
    uow.transaction_repository.get_by_id.return_value = None

    use_case = DeleteTransactionUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    with pytest.raises(ResourceNotFoundException) as exc_info:
        use_case.execute(id=999, current_user=current_user)

    assert str(exc_info.value) == "Transaction ID:999 doesn't exist."

    uow.transaction_repository.get_by_id.assert_called_once_with(999)
    uow.transaction_repository.delete.assert_not_called()

def test_delete_transaction_access_denied():
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

    use_case = DeleteTransactionUseCase(uow=uow)
    current_user = User(
        id=2, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    with pytest.raises(UnauthorizedException) as exc_info:
        use_case.execute(1, current_user)

    assert str(exc_info.value) == "Access denied for Transaction ID:1."

    uow.transaction_repository.get_by_id.assert_called_once_with(1)
    uow.transaction_repository.delete.assert_not_called()