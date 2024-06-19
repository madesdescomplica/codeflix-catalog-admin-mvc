from unittest.mock import MagicMock
from uuid import UUID

from faker import Faker
import pytest

from src.application.category.exceptions import InvalidCategory
from src.application.category.usecases import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse
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

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)

    def test_create_Category_with_invalid_data(self, mock_repository: CategoryRepository):
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(name="")

        with pytest.raises(InvalidCategory, match="name can not be empty or null") as exc_info:
            use_case.execute(request)

        assert exc_info.type is InvalidCategory
        assert str(exc_info.value) == "name can not be empty or null"

    def test_create_Category_call_repository_with_save_method(self, mock_repository: CategoryRepository):
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name=self.name,
            description=self.description,
            is_active=True  # default
        )

        use_case.execute(request)

        assert mock_repository.save.called is True

    def test_create_Category_do_not_call_repository_with_invalid_data(
        self,
        mock_repository: CategoryRepository
    ):
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(name="")

        with pytest.raises(InvalidCategory, match="name can not be empty or null") as exc_info:
            use_case.execute(request)

        assert exc_info.type is InvalidCategory
        assert str(exc_info.value) == "name can not be empty or null"
        assert mock_repository.save.called is False