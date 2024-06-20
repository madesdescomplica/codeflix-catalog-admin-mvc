from uuid import uuid4

from faker import Faker
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from infrastructure.category.repository import DjangoORMCategoryRepository
from src.domain.category import Category


@pytest.mark.django_db
class TestDeleteCategoryAPI:
    faker = Faker()

    @pytest.fixture
    def category_movie(self):
        return Category(
            name=self.faker.word(),
            description=self.faker.sentence()
        )

    @pytest.fixture
    def category_repository(self) -> DjangoORMCategoryRepository:
        return DjangoORMCategoryRepository()

    def test_should_DeleteCategoryAPI_return_400_if_category_does_not_exist(self):
        url = f"/api/categories/invalid_id/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_DeleteCategoryAPI_return_404_if_category_does_not_exist(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_DeleteCategoryAPI_return_204_if_category_exists(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_repository.list() == []
