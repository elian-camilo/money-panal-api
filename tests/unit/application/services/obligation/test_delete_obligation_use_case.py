import pytest
from unittest.mock import MagicMock
from datetime import date

from app.application.services.obligation_service import DeleteObligationUseCase
from app.domain.entities.obligation import Obligation
from app.domain.entities.user import User
from app.domain.exceptions import ResourceNotFoundException, UnauthorizedException

def test_delete_obligation_success():
    uow = MagicMock()
    fake_obligation = Obligation(
        id=1,
        name="Gym Membership",
        description="Monthly fee",
        amount=30.0,
        due_date=date(2027, 12, 31),
        is_paid=False,
        recurring=True,
        user_id=1,
        created_at=None
    )
    uow.obligation_repository.get_by_id.return_value = fake_obligation

    use_case = DeleteObligationUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    use_case.execute(1, current_user)

    uow.obligation_repository.get_by_id.assert_called_once_with(1)
    uow.obligation_repository.delete.assert_called_once_with(1)

def test_delete_obligation_not_found():
    uow = MagicMock()
    uow.obligation_repository.get_by_id.return_value = None

    use_case = DeleteObligationUseCase(uow=uow)
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
    uow.obligation_repository.delete.assert_not_called()

def test_delete_obligation_access_denied():
    uow = MagicMock()
    fake_obligation = Obligation(
        id=1,
        name="Gym Membership",
        description="Monthly fee",
        amount=30.0,
        due_date=date(2027, 12, 31),
        is_paid=False,
        recurring=True,
        user_id=1,
        created_at=None
    )
    uow.obligation_repository.get_by_id.return_value = fake_obligation

    use_case = DeleteObligationUseCase(uow=uow)
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
    uow.obligation_repository.delete.assert_not_called()
