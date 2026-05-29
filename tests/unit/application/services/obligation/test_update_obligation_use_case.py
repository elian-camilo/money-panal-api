import pytest
from unittest.mock import MagicMock
from datetime import date, timedelta

from app.application.services.obligation_service import UpdateObligationUseCase
from app.domain.entities.obligation import Obligation
from app.domain.entities.user import User
from app.domain.exceptions import (
    ResourceNotFoundException,
    UnauthorizedException,
    UnprocessableEntityException
)

def test_update_obligation_success():
    uow = MagicMock()
    future_date = date.today() + timedelta(days=5)
    fake_obligation = Obligation(
        id=1,
        name="Internet Bill",
        description="Fiber 300MB",
        amount=50.0,
        due_date=future_date,
        is_paid=False,
        recurring=False,
        user_id=1,
        created_at=None
    )
    uow.obligation_repository.get_by_id.return_value = fake_obligation

    use_case = UpdateObligationUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    obligation_to_update = Obligation(
        name="Internet Bill V2",
        description="Fiber 500MB",
        amount=60.0,
        due_date=future_date,
        is_paid=False,
        recurring=False,
        user_id=1
    )
    obligation_updated = Obligation(
        id=1,
        name="Internet Bill V2",
        description="Fiber 500MB",
        amount=60.0,
        due_date=future_date,
        is_paid=False,
        recurring=False,
        user_id=1,
        created_at=None
    )

    uow.obligation_repository.update.return_value = obligation_updated

    result = use_case.execute(id=1, obligation=obligation_to_update, current_user=current_user)

    assert result.name == "Internet Bill V2"
    assert result == obligation_updated

    uow.obligation_repository.get_by_id.assert_called_once_with(1)
    uow.obligation_repository.update.assert_called_once_with(1, obligation_to_update)

def test_update_obligation_not_found():
    uow = MagicMock()
    uow.obligation_repository.get_by_id.return_value = None

    use_case = UpdateObligationUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    future_date = date.today() + timedelta(days=5)
    obligation_to_update = Obligation(
        name="Internet Bill V2",
        description="Fiber 500MB",
        amount=60.0,
        due_date=future_date,
        is_paid=False,
        recurring=False,
        user_id=1
    )

    with pytest.raises(ResourceNotFoundException) as exc_info:
        use_case.execute(id=999, obligation=obligation_to_update, current_user=current_user)

    assert str(exc_info.value) == "Obligation ID:999 doesn't exist."
    uow.obligation_repository.get_by_id.assert_called_once_with(999)
    uow.obligation_repository.update.assert_not_called()

def test_update_obligation_access_denied():
    uow = MagicMock()
    future_date = date.today() + timedelta(days=5)
    fake_obligation = Obligation(
        id=1,
        name="Internet Bill",
        description="Fiber 300MB",
        amount=50.0,
        due_date=future_date,
        is_paid=False,
        recurring=False,
        user_id=1,
        created_at=None
    )
    uow.obligation_repository.get_by_id.return_value = fake_obligation

    use_case = UpdateObligationUseCase(uow=uow)
    current_user = User(
        id=2, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    obligation_to_update = Obligation(
        name="Internet Bill V2",
        description="Fiber 500MB",
        amount=60.0,
        due_date=future_date,
        is_paid=False,
        recurring=False,
        user_id=1
    )

    with pytest.raises(UnauthorizedException) as exc_info:
        use_case.execute(id=1, obligation=obligation_to_update, current_user=current_user)

    assert str(exc_info.value) == "Access denied for Obligation ID:1."
    uow.obligation_repository.get_by_id.assert_called_once_with(1)
    uow.obligation_repository.update.assert_not_called()

def test_update_obligation_due_date_in_past():
    uow = MagicMock()
    past_date = date.today() - timedelta(days=1)
    obligation_to_update = Obligation(
        name="Internet Bill V2",
        description="Fiber 500MB",
        amount=60.0,
        due_date=past_date,
        is_paid=False,
        recurring=False,
        user_id=1
    )

    use_case = UpdateObligationUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    with pytest.raises(UnprocessableEntityException) as exc_info:
        use_case.execute(id=1, obligation=obligation_to_update, current_user=current_user)

    assert str(exc_info.value) == "The due date don't be less than today."
    uow.obligation_repository.get_by_id.assert_not_called()
    uow.obligation_repository.update.assert_not_called()
