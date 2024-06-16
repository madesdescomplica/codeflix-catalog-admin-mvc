from unittest.mock import create_autospec
from uuid import uuid4

from faker import Faker
import pytest

from src.application.category.exceptions import CategoryNotFound
from src.application.category.usecases import UpdateCategory, UpdateCategoryRequest
from src.domain.category import Category, CategoryRepository


class TestUpdateCategory:
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

    def test_should_UpdateCategory_call_repository_with_get_by_id_method(
        self,
        category: Category,
        mock_repository: CategoryRepository
    ):
        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id)

        use_case.execute(request)

        assert mock_repository.get_by_id.called is True

    def test_should_UpdateCategory_raise_exception_when_category_not_found(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None
        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=uuid4())

        with pytest.raises(CategoryNotFound) as exc_info:
            use_case.execute(request)

        assert str(exc_info.value) == f"Category with id {request.id} not found"