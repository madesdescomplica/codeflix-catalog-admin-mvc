from uuid import uuid4

from faker import Faker
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from infrastructure.category.repository import DjangoORMCategoryRepository
from src.domain.category import Category


@pytest.mark.django_db
class TestUpdateCategoryAPI:
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

    def test_should_UpdateCategoryAPI_returns_400_if_payload_is_invalid(self):
        url = '/api/categories/invalid_id/'
        response = APIClient().put(
            url,
            data={
                "name": "",
                "description": self.faker.sentence(),
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."],
            "is_active": ["This field is required."],
        }

    def test_should_UpdateCategoryAPI_return_404_if_does_not_exist(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().put(
            url,
            data={
                "name": self.faker.word(),
                "description": self.faker.sentence(),
                "is_active": self.faker.boolean()
            },
            format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_UpdateCategoryAPI_if_payload_is_valid_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        updated_name = self.faker.word()
        updated_description = self.faker.sentence()
        updated_is_active = self.faker.boolean()

        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().put(
            url,
            data={
                "name": updated_name,
                "description": updated_description,
                "is_active": updated_is_active
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(category_movie.id)
        assert updated_category == Category(
            id=category_movie.id,
            name=updated_name,
            description=updated_description,
            is_active=updated_is_active
        )