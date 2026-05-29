import pytest
from unittest.mock import MagicMock
from datetime import date, timedelta

from app.application.services.obligation_service import CreateObligationUseCase
from app.domain.entities.obligation import Obligation
from app.domain.exceptions import UnprocessableEntityException

def test_create_obligation_success():
    uow = MagicMock()
    future_date = date.today() + timedelta(days=10)
    obligation_to_create = Obligation(
        name="Electricity Bill",
        description="Monthly power bill",
        amount=120.0,
        due_date=future_date,
        is_paid=False,
        recurring=False,
        user_id=1
    )
    obligation_saved = Obligation(
        id=1,
        name="Electricity Bill",
        description="Monthly power bill",
        amount=120.0,
        due_date=future_date,
        is_paid=False,
        recurring=False,
        user_id=1,
        created_at=None
    )
    uow.obligation_repository.save.return_value = obligation_saved

    use_case = CreateObligationUseCase(uow=uow)
    result = use_case.execute(obligation_to_create)

    assert result.id == 1
    assert result.name == "Electricity Bill"
    assert result == obligation_saved

    uow.obligation_repository.save.assert_called_once_with(obligation_to_create)

def test_create_obligation_due_date_in_past():
    uow = MagicMock()
    past_date = date.today() - timedelta(days=1)
    obligation = Obligation(
        name="Electricity Bill",
        description="Monthly power bill",
        amount=120.0,
        due_date=past_date,
        is_paid=False,
        recurring=False,
        user_id=1
    )

    use_case = CreateObligationUseCase(uow=uow)

    with pytest.raises(UnprocessableEntityException) as exc_info:
        use_case.execute(obligation)

    assert str(exc_info.value) == "The due date don't be less than today."
    uow.obligation_repository.save.assert_not_called()
