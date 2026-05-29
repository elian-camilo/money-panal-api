import pytest
from unittest.mock import MagicMock

from app.application.services.debt_service import CreateDebtUseCase
from app.domain.entities.debt import Debt


def test_create_debt_success():
    uow = MagicMock()

    fake_debt = Debt(
        id=1,
        person_name="Leo Messi",
        amount=1000.0,
        type="lend",
        due_date=None,
        is_settled=False,
        user_id=1,
        created_at=None
    )

    uow.debt_repository.save.return_value = fake_debt

    use_case = CreateDebtUseCase(uow=uow)
    debt_to_create = Debt(
        person_name="Leo Messi",
        amount=1000.0,
        type="lend",
        is_settled=False,
        user_id=1
    )
    result = use_case.execute(debt_to_create)

    assert result.id == 1
    assert result == fake_debt

    uow.debt_repository.save.assert_called_once_with(debt_to_create)
