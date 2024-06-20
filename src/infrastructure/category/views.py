from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED
)

from src.application.category.usecases import (
    CreateCategory,
    CreateCategoryRequest,
    ListCategory
)
from .repository import DjangoORMCategoryRepository
from .serializers import (
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer
)


class CategoryViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(DjangoORMCategoryRepository())
        output = use_case.execute(request)
        output_serializer = CreateCategoryResponseSerializer(output)

        return Response(
            status=HTTP_201_CREATED,
            data=output_serializer.data
        )

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