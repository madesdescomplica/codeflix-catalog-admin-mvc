from dataclasses import dataclass
from uuid import UUID

from src.domain.category import CategoryRepository


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
        self.repository.get_by_id(request.id)