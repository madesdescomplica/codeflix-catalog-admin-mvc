from uuid import uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_should_RetrieveAPI_return_400_if_id_is_not_valid(self):
        url = "/api/categories/invalid_id/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_RetrieveAPI_return_404_when_category_not_exists(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND