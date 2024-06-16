from faker import Faker
import pytest

from infrastructure.category.models import Category as CategoryModel
from src.infrastructure.category.repository import DjangoORMCategoryRepository
from src.domain.category import Category



@pytest.mark.django_db
class TestSave:
    faker = Faker()

    def test_save_category_in_database(self):
        category = Category(
            name=self.faker.word(),
            description=self.faker.sentence(),
            is_active=self.faker.boolean()
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category)
        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.get()
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active