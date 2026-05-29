import pytest
from unittest.mock import MagicMock

from app.application.services.debt_service import GetDebtUseCase
from app.domain.entities.debt import Debt
from app.domain.entities.user import User
from app.domain.exceptions import ResourceNotFoundException, UnauthorizedException


def test_get_debt_success():
    uow = MagicMock()

    fake_debt = Debt(
        id=1,
        person_name="Leo Messi",
        amount=1000.0,
        type="lend",
        is_settled=False,
        user_id=1,
        created_at=None
    )

    uow.debt_repository.get_by_id.return_value = fake_debt

    use_case = GetDebtUseCase(uow=uow)
    current_user = User(
        id=1,
        first_name="Leo",
        last_name="Messi",
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    result = use_case.execute(id=1, current_user=current_user)

    assert result.id == 1
    assert result.user_id == 1
    assert result == fake_debt

    uow.debt_repository.get_by_id.assert_called_once_with(1)


def test_get_debt_not_found():
    uow = MagicMock()

    uow.debt_repository.get_by_id.return_value = None

    use_case = GetDebtUseCase(uow=uow)
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

    assert str(exc_info.value) == "Debt ID:999 doesn't exist."
    uow.debt_repository.get_by_id.assert_called_once_with(999)


def test_get_debt_access_denied():
    uow = MagicMock()

    fake_debt = Debt(
        id=1,
        person_name="Leo Messi",
        amount=1000.0,
        type="lend",
        is_settled=False,
        user_id=1,
        created_at=None
    )

    uow.debt_repository.get_by_id.return_value = fake_debt

    use_case = GetDebtUseCase(uow=uow)
    current_user = User(
        id=2,
        first_name="Cristiano",
        last_name="Ronaldo",
        email="cr7@cr7.com",
        password="password_123",
        created_at=None
    )

    with pytest.raises(UnauthorizedException) as exc_info:
        use_case.execute(id=1, current_user=current_user)

    assert str(exc_info.value) == "You don't have access to this resource."
    uow.debt_repository.get_by_id.assert_called_once_with(1)
