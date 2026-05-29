import pytest
from unittest.mock import MagicMock

from app.application.services.debt_service import UpdateDebtUseCase
from app.domain.entities.debt import Debt
from app.domain.entities.user import User
from app.domain.exceptions import ResourceNotFoundException, UnauthorizedException


def test_update_debt_success():
    uow = MagicMock()

    existing_debt = Debt(
        id=1,
        person_name="Leo Messi",
        amount=1000.0,
        type="lend",
        is_settled=False,
        user_id=1,
        created_at=None
    )

    updated_debt = Debt(
        id=1,
        person_name="Leo Messi",
        amount=1500.0,
        type="lend",
        is_settled=True,
        user_id=1,
        created_at=None
    )

    uow.debt_repository.get_by_id.return_value = existing_debt
    uow.debt_repository.update.return_value = updated_debt

    use_case = UpdateDebtUseCase(uow=uow)
    current_user = User(
        id=1,
        first_name="Leo",
        last_name="Messi",
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    debt_data_to_update = Debt(
        person_name="Leo Messi",
        amount=1500.0,
        type="lend",
        is_settled=True,
        user_id=1
    )

    result = use_case.execute(id=1, debt=debt_data_to_update, current_user=current_user)

    assert result.id == 1
    assert result.amount == 1500.0
    assert result.is_settled is True
    uow.debt_repository.get_by_id.assert_called_once_with(1)
    uow.debt_repository.update.assert_called_once_with(1, debt_data_to_update)


def test_update_debt_not_found():
    uow = MagicMock()

    uow.debt_repository.get_by_id.return_value = None

    use_case = UpdateDebtUseCase(uow=uow)
    current_user = User(
        id=1,
        first_name="Leo",
        last_name="Messi",
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    debt_data = Debt(
        person_name="Leo Messi",
        amount=1500.0,
        type="lend",
        is_settled=True,
        user_id=1
    )

    with pytest.raises(ResourceNotFoundException) as exc_info:
        use_case.execute(id=999, debt=debt_data, current_user=current_user)

    assert str(exc_info.value) == "Debt ID:999 doesn't exist."
    uow.debt_repository.get_by_id.assert_called_once_with(999)
    uow.debt_repository.update.assert_not_called()


def test_update_debt_access_denied():
    uow = MagicMock()

    existing_debt = Debt(
        id=1,
        person_name="Leo Messi",
        amount=1000.0,
        type="lend",
        is_settled=False,
        user_id=1,
        created_at=None
    )

    uow.debt_repository.get_by_id.return_value = existing_debt

    use_case = UpdateDebtUseCase(uow=uow)
    current_user = User(
        id=2,
        first_name="Cristiano",
        last_name="Ronaldo",
        email="cr7@cr7.com",
        password="password_123",
        created_at=None
    )

    debt_data = Debt(
        person_name="Leo Messi",
        amount=1500.0,
        type="lend",
        is_settled=True,
        user_id=1
    )

    with pytest.raises(UnauthorizedException) as exc_info:
        use_case.execute(id=1, debt=debt_data, current_user=current_user)

    assert str(exc_info.value) == "You don't have access to this resource."
    uow.debt_repository.get_by_id.assert_called_once_with(1)
    uow.debt_repository.update.assert_not_called()
