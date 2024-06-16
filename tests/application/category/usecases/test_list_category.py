from unittest.mock import create_autospec

from faker import Faker
import pytest

from src.application.category.usecases import ListCategory
from src.domain.category import Category, CategoryRepository


class TestListCategory:
    faker = Faker()

    @pytest.fixture
    def category(self) -> Category:
        return Category(
            name=self.faker.word(),
            description=self.faker.sentence(),
            is_active=self.faker.boolean()
        )

    @pytest.fixture
    def mock_repository(self) -> CategoryRepository:
        return create_autospec(CategoryRepository, instance=True)


    def test_should_ListCategory_call_repository_with_list_method(
        self,
        mock_repository: CategoryRepository
    ):
        use_case = ListCategory(repository=mock_repository)

        use_case.execute()

        assert mock_repository.list.called is True

    def test_should_ListCategory_return_an_empty_list(
        self,
        mock_repository: CategoryRepository
    ):
        mock_repository.list.return_value = []
        use_case = ListCategory(repository=mock_repository)

        response = use_case.execute()

        assert response.data == []
