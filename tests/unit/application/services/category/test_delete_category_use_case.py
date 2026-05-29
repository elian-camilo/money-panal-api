import pytest
from unittest.mock import MagicMock

from app.application.services.category_service import DeleteCategoryUseCase
from app.domain.entities.caterogy import Category
from app.domain.entities.user import User
from app.domain.exceptions import ResourceNotFoundException, UnauthorizedException

def test_delete_category_success():
    uow = MagicMock()
    fake_category = Category(
        id=1,
        name="Food",
        description="Daily meals",
        user_id=1,
        created_at=None
    )
    uow.category_repository.get_by_id.return_value = fake_category

    use_case = DeleteCategoryUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )

    use_case.execute(1, current_user)

    uow.category_repository.get_by_id.assert_called_once_with(1)
    uow.category_repository.delete.assert_called_once_with(1)

def test_delete_category_not_found():
    uow = MagicMock()
    uow.category_repository.get_by_id.return_value = None

    use_case = DeleteCategoryUseCase(uow=uow)
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

    assert str(exc_info.value) == "Category ID:999 doesn't exist."

    uow.category_repository.get_by_id.assert_called_once_with(999)
    uow.category_repository.delete.assert_not_called()

def test_delete_category_access_denied():
    uow = MagicMock()
    fake_category = Category(
        id=1,
        name="Food",
        description="Daily meals",
        user_id=1,
        created_at=None
    )
    uow.category_repository.get_by_id.return_value = fake_category

    use_case = DeleteCategoryUseCase(uow=uow)
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

    assert str(exc_info.value) == "Access denied for Category ID:1."

    uow.category_repository.get_by_id.assert_called_once_with(1)
    uow.category_repository.delete.assert_not_called()
