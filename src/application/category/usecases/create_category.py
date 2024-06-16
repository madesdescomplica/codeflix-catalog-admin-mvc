from dataclasses import dataclass
from uuid import UUID

from src.domain.category import Category, CategoryRepository


@dataclass
class CreateCategoryRequest:
    name: str
    description: str = ""
    is_active: bool = True

@dataclass
class CreateCategoryResponse:
    id: UUID

@dataclass
class CreateCategory:
    repository: CategoryRepository

    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        category = Category(
            name=request.name,
            description=request.description,
            is_active=request.is_active
        )

        return category.id