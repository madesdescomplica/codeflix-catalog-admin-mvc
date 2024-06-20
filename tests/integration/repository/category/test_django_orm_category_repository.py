from faker import Faker
import pytest

from infrastructure.category.models import Category as CategoryModel
from infrastructure.category.repository import DjangoORMCategoryRepository
from src.domain.category import Category


@pytest.mark.django_db
class TestDjangoORMCategoryRepository:
    faker = Faker()

    @pytest.fixture
    def category(self):
        return Category(
            name=self.faker.word(),
            description=self.faker.sentence(),
            is_active=self.faker.boolean()
        )

    @pytest.fixture
    def other_category(self):
        return Category(
            name=self.faker.word(),
            description=self.faker.sentence(),
            is_active=self.faker.boolean()
        )

    @pytest.fixture
    def repository(self):
        return DjangoORMCategoryRepository()

    def test_save_category_in_database(
        self,
        category: Category,
        repository: DjangoORMCategoryRepository
    ):
        assert CategoryModel.objects.count() == 0
        repository.save(category)
        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.get()
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active

    def test_get_category_in_database(
        self,
        category: Category,
        repository: DjangoORMCategoryRepository
    ):
        assert CategoryModel.objects.count() == 0
        repository.save(category)
        assert CategoryModel.objects.count() == 1

        category_db = repository.get_by_id(category.id)
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active

    def test_list_categories_in_database(
        self,
        category: Category,
        other_category: Category,
        repository: DjangoORMCategoryRepository
    ):
        assert CategoryModel.objects.count() == 0
        repository.save(category)
        repository.save(other_category)
        assert CategoryModel.objects.count() == 2

        category_db = repository.list()
        assert category_db == [category, other_category]