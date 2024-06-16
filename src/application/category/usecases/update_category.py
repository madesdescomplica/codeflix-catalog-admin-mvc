from dataclasses import dataclass
from uuid import UUID

from src.domain.category import CategoryRepository
from ..exceptions import CategoryNotFound, InvalidCategory


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


@dataclass
class UpdateCategory:
    repository: CategoryRepository

    def execute(self, request: UpdateCategoryRequest) -> None:
        """
            - Busca categoria pelo ID
            - Atualiza categoria com os valores passados
            - Ativar/Desativar categoria
            - Salva categoria
        """
        category = self.repository.get_by_id(request.id)

        if category is None:
            raise CategoryNotFound(f"Category with id {request.id} not found")

        try:
            current_name = category.name
            current_description = category.description

            if request.name is not None:
                current_name = request.name

            if request.description is not None:
                current_description = request.description

            category.update_category(
                name=current_name,
                description=current_description
            )
        except ValueError as e:
            raise InvalidCategory(e)