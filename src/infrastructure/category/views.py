from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)

from src.application.category.exceptions import CategoryNotFound
from src.application.category.usecases import (
    CreateCategory,
    CreateCategoryRequest,
    DeleteCategory,
    DeleteCategoryRequest,
    GetCategory,
    GetCategoryRequest,
    ListCategory,
    UpdateCategory,
    UpdateCategoryRequest
)
from infrastructure.category.repository import DjangoORMCategoryRepository
from infrastructure.category.schema_extensions import category_viewset_schema
from infrastructure.category.serializers import (
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    DeleteCategoryRequestSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
    ListCategoryResponseSerializer,
    UpdateCategoryRequestSerializer
)

@category_viewset_schema
class CategoryViewSet(viewsets.ViewSet):

    def list(self, request: Request) -> Response:
        usecase = ListCategory(repository=DjangoORMCategoryRepository())
        response = usecase.execute()
        serializer = ListCategoryResponseSerializer(instance=response)

        return Response(
            status=HTTP_200_OK,
            data=serializer.data
        )

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

    def update(self, request: Request, pk: None) -> Response:
        serializer = UpdateCategoryRequestSerializer(
            data={
                **request.data,
                "id": pk
            }
        )
        serializer.is_valid(raise_exception=True)

        request = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk: None) -> Response:
        serializer = DeleteCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(DeleteCategoryRequest(**serializer.validated_data))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)
