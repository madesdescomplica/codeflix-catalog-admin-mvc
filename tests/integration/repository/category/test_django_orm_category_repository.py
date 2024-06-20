from faker import Faker
import pytest

from infrastructure.category.models import CategoryModel
from infrastructure.category.repository import DjangoORMCategoryRepository
from src.domain.category import Category


@pytest.mark.django_db
class TestDjangoORMCategoryRepository:
    faker = Faker()

    @pytest.fixture
    def category(self) -> Category:
        return Category(
            name=self.faker.word(),
            description=self.faker.sentence(),
            is_active=self.faker.boolean()
        )

    @pytest.fixture
    def other_category(self) -> Category:
        return Category(
            name=self.faker.word(),
            description=self.faker.sentence(),
            is_active=self.faker.boolean()
        )

    @pytest.fixture
    def category_model(self, category: Category) -> CategoryModel:
        return CategoryModel(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )

    @pytest.fixture
    def other_category_model(self, other_category: Category) -> CategoryModel:
        return CategoryModel(
            id=other_category.id,
            name=other_category.name,
            description=other_category.description,
            is_active=other_category.is_active
        )

    @pytest.fixture
    def repository(self):
        return DjangoORMCategoryRepository()

    def test_list_categories_in_database(
        self,
        category: Category,
        other_category: Category,
        category_model: CategoryModel,
        other_category_model: CategoryModel,
        repository: DjangoORMCategoryRepository
    ):
        assert CategoryModel.objects.count() == 0
        category_model.save()
        other_category_model.save()
        assert CategoryModel.objects.count() == 2

        category_db = repository.list()
        assert category_db == [category, other_category]

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
        category_model: CategoryModel,
        other_category_model: CategoryModel,
        repository: DjangoORMCategoryRepository
    ):
        assert CategoryModel.objects.count() == 0
        category_model.save()
        other_category_model.save()
        assert CategoryModel.objects.count() == 2

        category_db = repository.get_by_id(category.id)
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active

    def test_update_category_in_database(
        self,
        category: Category,
        category_model: CategoryModel,
        other_category_model: CategoryModel,
        repository: DjangoORMCategoryRepository
    ):
        assert CategoryModel.objects.count() == 0
        category_model.save()
        other_category_model.save()
        assert CategoryModel.objects.count() == 2

        category_updated = Category(
            id=category.id,
            name=self.faker.word(),
            description=self.faker.sentence(),
            is_active=self.faker.boolean()
        )

        repository.update(category_updated)

        category_db = CategoryModel.objects.get(id=category.id)

        assert category_db.id == category.id
        assert category_db.name == category_updated.name
        assert category_db.description == category_updated.description
        assert category_db.is_active == category_updated.is_active

    def test_delete_category_in_database(
        self,
        category: Category,
        other_category: Category,
        category_model: CategoryModel,
        other_category_model: CategoryModel,
        repository: DjangoORMCategoryRepository
    ):
        assert CategoryModel.objects.count() == 0
        category_model.save()
        other_category_model.save()
        assert CategoryModel.objects.count() == 2

        repository.delete(category.id)
        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.all()[0]

        assert category_db.id == other_category.id
        assert category_db.name == other_category.name
        assert category_db.description == other_category.description
        assert category_db.is_active == other_category.is_active
