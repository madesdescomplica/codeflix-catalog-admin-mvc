from unittest.mock import MagicMock
from uuid import UUID

from faker import Faker
import pytest

from src.application.category.usecases import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.domain.category import CategoryRepository


class TestCreateCategory:
    faker = Faker()
    name=faker.word()
    description=faker.sentence()

    @pytest.fixture
    def mock_repository(self) -> CategoryRepository:
        return MagicMock(CategoryRepository)

    def test_create_Category_with_valid_data(self, mock_repository: CategoryRepository):
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name=self.name,
            description=self.description,
            is_active=True  # default
        )

        category_id = use_case.execute(request)

        assert category_id is not None
        assert isinstance(category_id, UUID)