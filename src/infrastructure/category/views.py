from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND
)

from src.application.category.exceptions import CategoryNotFound
from src.application.category.usecases import (
    CreateCategory,
    CreateCategoryRequest,
    GetCategory,
    GetCategoryRequest,
    ListCategory
)
from .repository import DjangoORMCategoryRepository
from .serializers import (
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer
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

    def retrieve(self, request: Request, pk: None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            request = GetCategoryRequest(serializer.validated_data["id"])
            response = use_case.execute(request)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_out = RetrieveCategoryResponseSerializer(instance=response)

        return Response(
            status=HTTP_200_OK,
            data=category_out.data
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