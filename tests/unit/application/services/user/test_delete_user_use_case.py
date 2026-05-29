import pytest
from unittest.mock import MagicMock

from app.application.services.user_service import DeleteUserUseCase
from app.domain.entities.user import User
from app.domain.exceptions import ResourceNotFoundException, UnauthorizedException


def test_delete_user_success():
    uow = MagicMock()
    fake_user = User(
        id=1,
        first_name="Leo",
        last_name="Messi",
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    uow.user_repository.get_by_id.return_value = fake_user

    use_case = DeleteUserUseCase(uow=uow)
    current_user = User(
        id=1,
        first_name="Leo",
        last_name="Messi",
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    use_case.execute(id=1, current_user=current_user)

    uow.user_repository.get_by_id.assert_called_once_with(1)
    uow.user_repository.delete.assert_called_once_with(1)


def test_delete_user_not_found():
    uow = MagicMock()
    uow.user_repository.get_by_id.return_value = None

    use_case = DeleteUserUseCase(uow=uow)
    current_user = User(
        id=1,
        first_name="Leo",
        last_name="Messi",
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    with pytest.raises(ResourceNotFoundException) as exc_info:
        use_case.execute(id=1, current_user=current_user)

    assert str(exc_info.value) == "User ID:1 doesn't exist."
    uow.user_repository.get_by_id.assert_called_once_with(1)
    uow.user_repository.delete.assert_not_called()


def test_delete_user_access_denied():
    uow = MagicMock()
    use_case = DeleteUserUseCase(uow=uow)
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
    uow.user_repository.get_by_id.assert_not_called()
    uow.user_repository.delete.assert_not_called()
