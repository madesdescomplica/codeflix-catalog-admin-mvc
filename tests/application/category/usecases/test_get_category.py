from unittest.mock import create_autospec
from uuid import uuid4

from faker import Faker
import pytest

from src.application.category.exceptions import CategoryNotFound
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

    def test_GetCategory_raise_exception_when_category_id_does_not_exist(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None
        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=uuid4())

        with pytest.raises(CategoryNotFound) as exc_info:
            use_case.execute(request)

        assert str(exc_info.value) == f"Category with id {request.id} not found"

    def test_GetCategory_exists_then_return_response_dto(
        self,
        mock_repository: CategoryRepository,
        category: Category
    ):
        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=category.id)

        response = use_case.execute(request)

        assert response.id == category.id
        assert response.name == category.name
        assert response.description == category.description
        assert response.is_active == category.is_active