from uuid import UUID
from faker import Faker
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.infrastructure.category.repository import DjangoORMCategoryRepository
from src.domain.category import Category


@pytest.mark.django_db
class TestCreateCategoryAPI:
    faker = Faker()

    @pytest.fixture
    def category_repository(self) -> DjangoORMCategoryRepository:
        return DjangoORMCategoryRepository()

    def test_should_CreateCategoryAPI_return_400_if_payload_is_invalid(self):
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "",
                "description": self.faker.sentence()
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."]
        }

    def test_should_CreateCategoryAPI_create_category_and_return_201_if_payload_is_valid(
        self,
        category_repository: DjangoORMCategoryRepository
    ):
        name = self.faker.word()
        description = self.faker.sentence()
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": name,
                "description": description
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_category_id = UUID(response.data["id"])

        assert category_repository.get_by_id(created_category_id) == Category(
            id=created_category_id,
            name=name,
            description=description
        )

        assert category_repository.list() == [
            Category(
                id=created_category_id,
                name=name,
                description=description
            )
        ]