from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from infrastructure.category.repository import DjangoORMCategoryRepository
from src.application.category.usecases import ListCategory


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        usecase = ListCategory(repository=DjangoORMCategoryRepository())
        output = usecase.execute()

        categories = [
            {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active
            } for category in output.data
        ]

        return Response(
            status=HTTP_200_OK,
            data=categories
        )