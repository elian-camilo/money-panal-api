import pytest
from unittest.mock import MagicMock

from app.application.services.user_service import ListUserUseCase
from app.domain.entities.user import User
from app.domain.exceptions import UnauthorizedException


def test_list_user_access_denied():
    uow = MagicMock()
    use_case = ListUserUseCase(uow=uow)
    current_user = User(
        id=1,
        first_name="Leo",
        last_name="Messi",
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    with pytest.raises(UnauthorizedException) as exc_info:
        use_case.execute(offset=0, limit=10, current_user=current_user)

    assert str(exc_info.value) == "You don't have permission to list users."
    uow.user_repository.get_all.assert_not_called()
