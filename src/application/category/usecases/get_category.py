from dataclasses import dataclass
from uuid import UUID

from src.domain.category import CategoryRepository


@dataclass
class GetCategoryRequest:
    id: UUID

@dataclass
class GetCategoryResponse:
    id: UUID
    name: str
    description: str
    is_active: bool

@dataclass
class GetCategory:
    repository: CategoryRepository

    def execute(self, request: GetCategoryRequest) -> GetCategoryResponse:
        self.repository.get_by_id(request.id)