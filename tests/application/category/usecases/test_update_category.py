from unittest.mock import create_autospec
from uuid import uuid4

from faker import Faker
import pytest

from src.application.category.exceptions import CategoryNotFound, InvalidCategory
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

    def test_should_UpdateCategory_updates_name(
        self,
        category: Category,
        mock_repository: CategoryRepository
    ):
        updated_name = self.faker.word()
        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, name=updated_name)

        use_case.execute(request)

        assert category.name == updated_name

    def test_should_UpdateCategory_raises_exception_when_name_is_invalid(
        self,
        category: Category,
        mock_repository: CategoryRepository
    ):
        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, name="")

        with pytest.raises(InvalidCategory, match="name can not be empty or null"):
            use_case.execute(request)

    def test_should_UpdateCategory_updates_description(
        self,
        category: Category,
        mock_repository: CategoryRepository
    ):
        updated_description = self.faker.sentence()
        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, description=updated_description)

        use_case.execute(request)

        assert category.description == updated_description

    def test_should_UpdateCategory_updates_name_and_description(
        self,
        category: Category,
        mock_repository: CategoryRepository
    ):
        updated_name = self.faker.word()
        updated_description = self.faker.sentence()
        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name=updated_name,
            description=updated_description
        )

        use_case.execute(request)

        assert category.name == updated_name
        assert category.description == updated_description