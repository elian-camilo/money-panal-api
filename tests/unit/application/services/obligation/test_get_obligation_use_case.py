import pytest
from unittest.mock import MagicMock
from datetime import date

from app.application.services.obligation_service import GetObligationUseCase
from app.domain.entities.obligation import Obligation
from app.domain.entities.user import User
from app.domain.exceptions import ResourceNotFoundException, UnauthorizedException

def test_get_obligation_success():
    uow = MagicMock()
    fake_obligation = Obligation(
        id=1,
        name="Credit Card",
        description="Minimum payment",
        amount=250.0,
        due_date=date(2027, 12, 31),
        is_paid=False,
        recurring=False,
        user_id=1,
        created_at=None
    )
    uow.obligation_repository.get_by_id.return_value = fake_obligation

    use_case = GetObligationUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    result = use_case.execute(1, current_user)

    assert result.name == "Credit Card"
    assert result == fake_obligation
    uow.obligation_repository.get_by_id.assert_called_once_with(1)

def test_get_obligation_not_found():
    uow = MagicMock()
    uow.obligation_repository.get_by_id.return_value = None

    use_case = GetObligationUseCase(uow=uow)
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

    assert str(exc_info.value) == "Obligation ID:999 doesn't exist."
    uow.obligation_repository.get_by_id.assert_called_once_with(999)

def test_get_obligation_access_denied():
    uow = MagicMock()
    fake_obligation = Obligation(
        id=1,
        name="Credit Card",
        description="Minimum payment",
        amount=250.0,
        due_date=date(2027, 12, 31),
        is_paid=False,
        recurring=False,
        user_id=1,
        created_at=None
    )
    uow.obligation_repository.get_by_id.return_value = fake_obligation

    use_case = GetObligationUseCase(uow=uow)
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

    assert str(exc_info.value) == "Access denied for Obligation ID:1."
    uow.obligation_repository.get_by_id.assert_called_once_with(1)
