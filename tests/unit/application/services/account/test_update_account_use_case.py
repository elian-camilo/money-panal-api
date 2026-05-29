import pytest
from unittest.mock import MagicMock

from app.application.services.account_service import UpdateAccountUseCase
from app.domain.entities.account import Account
from app.domain.entities.user import User
from app.domain.exceptions import ResourceNotFoundException, UnauthorizedException

def test_update_account_success():
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
    uow.account_repository.get_by_id.return_value = fake_account

    use_case = UpdateAccountUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    account_to_update = Account(
        name="Credit Card",
        amount=1000.0,
        profit_percentage=0.0,
        currency="usd",
        user_id=1
    )
    account_updated = Account(
        id=1,
        name="Credit Card",
        amount=1000.0,
        profit_percentage=0.0,
        currency="usd",
        user_id=1,
        created_at=None
    )

    uow.account_repository.update.return_value = account_updated

    result = use_case.execute(id=1, account=account_to_update, current_user=current_user)

    assert result.name == "Credit Card"
    assert result == account_updated

    uow.account_repository.get_by_id.assert_called_once_with(1)
    uow.account_repository.update.assert_called_once_with(1, account_to_update)

def test_update_account_not_found():
    uow = MagicMock()
    uow.account_repository.get_by_id.return_value = None

    use_case = UpdateAccountUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    account_to_update = Account(
        name="Credit Card",
        amount=1000.0,
        profit_percentage=0.0,
        currency="usd",
        user_id=1
    )

    with pytest.raises(ResourceNotFoundException) as exc_info:
        use_case.execute(id=999, account=account_to_update, current_user=current_user)

    assert str(exc_info.value) == "Account ID:999 doesn't exist."

    uow.account_repository.get_by_id.assert_called_once_with(999)
    uow.account_repository.update.assert_not_called()

def test_update_account_access_denied():
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
    uow.account_repository.get_by_id.return_value = fake_account

    use_case = UpdateAccountUseCase(uow=uow)
    current_user = User(
        id=2,
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    account_to_update = Account(
        name="Credit Card",
        amount=1000.0,
        profit_percentage=0.0,
        currency="usd",
        user_id=1
    )

    with pytest.raises(UnauthorizedException) as exc_info:
        use_case.execute(id=1, account=account_to_update, current_user=current_user)

    assert str(exc_info.value) == "Access denied for Account ID:1."

    uow.account_repository.get_by_id.assert_called_once_with(1)
    uow.account_repository.update.assert_not_called()
