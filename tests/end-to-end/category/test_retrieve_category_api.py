from uuid import uuid4

from faker import Faker
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from infrastructure.category.repository import DjangoORMCategoryRepository
from src.domain.category import Category


@pytest.mark.django_db
class TestRetrieveAPI:
    faker = Faker()

    @pytest.fixture
    def category_movie(self):
        return Category(
            name=self.faker.word(),
            description=self.faker.sentence()
        )

    @pytest.fixture
    def category_documentary(self):
        return Category(
            name=self.faker.word(),
            description=self.faker.sentence()
        )

    @pytest.fixture
    def category_repository(self) -> DjangoORMCategoryRepository:
        return DjangoORMCategoryRepository()

    def test_should_RetrieveAPI_return_400_if_id_is_not_valid(self):
        url = "/api/categories/invalid_id/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_RetrieveAPI_return_404_when_category_not_exists(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_RetrieveAPI_return_category_if_exists(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = f"/api/categories/{category_documentary.id}/"
        response = APIClient().get(url)
        expected_data = {
            "data": {
                "id": str(category_documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data