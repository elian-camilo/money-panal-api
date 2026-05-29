import pytest
from unittest.mock import MagicMock

from app.application.services.category_service import CreateCategoryUseCase
from app.domain.entities.caterogy import Category

def test_create_category_success():
    uow = MagicMock()

    fake_category = Category(
        id=1,
        name="Food",
        description="Daily meals",
        user_id=1,
        created_at=None
    )

    uow.category_repository.save.return_value = fake_category

    use_case = CreateCategoryUseCase(uow=uow)
    category_to_create = Category(
        name="Food",
        description="Daily meals",
        user_id=1
    )
    result = use_case.execute(category_to_create, user_id=1)

    assert result.id == 1
    assert result == fake_category

    uow.category_repository.save.assert_called_once_with(category_to_create)
