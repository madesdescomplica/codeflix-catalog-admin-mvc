from dataclasses import dataclass

from src.domain.category import Category, CategoryRepository


@dataclass
class ListCategoryResponse:
    data: list[Category]

@dataclass
class ListCategory:
    repository: CategoryRepository

    def execute(self) -> ListCategoryResponse:
        self.repository.list()