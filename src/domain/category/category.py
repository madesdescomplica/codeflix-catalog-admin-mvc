from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Category:
    name: str
    description: str = ""
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.name:
            raise ValueError("name can not be empty or null")