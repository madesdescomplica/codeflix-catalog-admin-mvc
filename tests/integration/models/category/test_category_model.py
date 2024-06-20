from uuid import UUID

from django.forms import ValidationError
from faker import Faker
import pytest

from infrastructure.category.models import CategoryModel


@pytest.mark.django_db
class TestCategoryModel:
    faker = Faker()
    name = faker.word()
    description = faker.sentence()
    is_active = faker.boolean()

    def test_create_category(self):
        category = CategoryModel.objects.create(
            name=self.name,
            description=self.description,
            is_active=self.is_active
        )

        assert isinstance(category, CategoryModel)
        assert category.name == self.name
        assert category.description == self.description
        assert category.is_active == self.is_active
        assert isinstance(category.id, UUID)

    def test_category_str(self):
        category = CategoryModel(name=self.name)

        assert str(category) == self.name

    def test_default_is_active(self):
        category = CategoryModel.objects.create(name=self.name)

        assert category.is_active is True

    def test_name_max_length(self):
        name = self.faker.sentence(nb_words=100)

        category = CategoryModel(name=name)
        with pytest.raises(ValidationError):
            category.full_clean()