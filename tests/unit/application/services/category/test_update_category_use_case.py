import pytest
from unittest.mock import MagicMock

from app.application.services.category_service import UpdateCategoryUseCase
from app.domain.entities.caterogy import Category
from app.domain.entities.user import User
from app.domain.exceptions import ResourceNotFoundException, UnauthorizedException

def test_update_category_success():
    uow = MagicMock()
    fake_category = Category(
        id=1,
        name="Food",
        description="Daily meals",
        user_id=1,
        created_at=None
    )
    uow.category_repository.get_by_id.return_value = fake_category

    use_case = UpdateCategoryUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    category_to_update = Category(
        name="Entertainment",
        description="Movies and games",
        user_id=1
    )
    category_updated = Category(
        id=1,
        name="Entertainment",
        description="Movies and games",
        user_id=1,
        created_at=None
    )

    uow.category_repository.update.return_value = category_updated

    result = use_case.execute(id=1, category=category_to_update, current_user=current_user)

    assert result.name == "Entertainment"
    assert result == category_updated

    uow.category_repository.get_by_id.assert_called_once_with(1)
    uow.category_repository.update.assert_called_once_with(1, category_to_update)

def test_update_category_not_found():
    uow = MagicMock()
    uow.category_repository.get_by_id.return_value = None

    use_case = UpdateCategoryUseCase(uow=uow)
    current_user = User(
        id=1, 
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    category_to_update = Category(
        name="Entertainment",
        description="Movies and games",
        user_id=1
    )

    with pytest.raises(ResourceNotFoundException) as exc_info:
        use_case.execute(id=999, category=category_to_update, current_user=current_user)

    assert str(exc_info.value) == "Category ID:999 doesn't exist."

    uow.category_repository.get_by_id.assert_called_once_with(999)
    uow.category_repository.update.assert_not_called()

def test_update_category_access_denied():
    uow = MagicMock()
    fake_category = Category(
        id=1,
        name="Food",
        description="Daily meals",
        user_id=1,
        created_at=None
    )
    uow.category_repository.get_by_id.return_value = fake_category

    use_case = UpdateCategoryUseCase(uow=uow)
    current_user = User(
        id=2,
        first_name="Leo", 
        last_name="Messi", 
        email="leo@messi.com",
        password="password_123",
        created_at=None
    )
    category_to_update = Category(
        name="Entertainment",
        description="Movies and games",
        user_id=1
    )
    with pytest.raises(UnauthorizedException) as exc_info:
        use_case.execute(id=1, category=category_to_update, current_user=current_user)

    assert str(exc_info.value) == "Access denied for Category ID:1."

    uow.category_repository.get_by_id.assert_called_once_with(1)
    uow.category_repository.update.assert_not_called()
