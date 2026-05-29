import pytest
from unittest.mock import MagicMock

from app.application.services.account_service import DeleteAccountUseCase
from app.domain.entities.account import Account
from app.domain.entities.user import User
from app.domain.exceptions import ResourceNotFoundException, UnauthorizedException

def test_delete_account_success():
    uow = MagicMock()
    fake_account = Account(
        id=1,
        name="Savings",
        amount=1200.0,
        profit_percentage=2.0,
        currency="cop",
        user_id=1,
        created_at=None
    )
    uow.account_repository.get_by_id.return_value = fake_account

    use_case = DeleteAccountUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    use_case.execute(1, current_user)

    uow.account_repository.get_by_id.assert_called_once_with(1)
    uow.account_repository.delete.assert_called_once_with(1)

def test_delete_account_not_found():
    uow = MagicMock()
    uow.account_repository.get_by_id.return_value = None

    use_case = DeleteAccountUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    with pytest.raises(ResourceNotFoundException) as exc_info:
        use_case.execute(999, current_user)

    assert str(exc_info.value) == "Account ID:999 doesn't exist."

    uow.account_repository.get_by_id.assert_called_once_with(999)
    uow.account_repository.delete.assert_not_called()

def test_delete_account_access_denied():
    uow = MagicMock()
    fake_account = Account(
        id=1,
        name="Savings",
        amount=1200.0,
        profit_percentage=2.0,
        currency="cop",
        user_id=1,
        created_at=None
    )
    uow.account_repository.get_by_id.return_value = fake_account

    use_case = DeleteAccountUseCase(uow=uow)
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

    assert str(exc_info.value) == "Access denied for Account ID:1."

    uow.account_repository.get_by_id.assert_called_once_with(1)
    uow.account_repository.delete.assert_not_called()
