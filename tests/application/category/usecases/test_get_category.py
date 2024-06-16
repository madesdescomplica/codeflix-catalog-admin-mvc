from unittest.mock import create_autospec
from faker import Faker
import pytest

from src.application.category.usecases import GetCategory, GetCategoryRequest
from src.domain.category import Category, CategoryRepository


class TestGetCategory:
    faker = Faker()
    name = faker.word()
    description = faker.sentence()
    is_active = faker.boolean()

    @pytest.fixture
    def category(self) -> Category:
        return Category(
            name=self.name,
            description=self.description,
            is_active=self.is_active
        )

    @pytest.fixture
    def mock_repository(self, category: Category) -> CategoryRepository:
        repository = create_autospec(CategoryRepository, instance=True)
        repository.get_by_id.return_value = category
        return repository

    def test_GetCategory_call_repository_with_get_by_id_method(
        self,
        mock_repository: CategoryRepository,
        category: Category
    ):
        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=category.id)

        use_case.execute(request)

        assert mock_repository.get_by_id.called is True