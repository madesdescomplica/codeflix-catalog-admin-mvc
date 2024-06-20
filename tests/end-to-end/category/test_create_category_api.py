from faker import Faker
import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateCategoryAPI:
    faker = Faker()

    def test_CategoryViewSet_return_400_if_payload_is_invalid(self):
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