from uuid import UUID, uuid4

from faker import Faker
import pytest

from src.domain.category import Category


class TestCategory:
    faker = Faker()
    name = faker.word()

    def test_Category_must_be_created_with_id_as_uuid4(self):
        category = Category(name=self.name)

        assert isinstance(category.id, UUID)

    def test_Category_must_have_the_required_name(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

    def test_Category_can_not_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name can not be empty or null"):
            Category(name="")

    def test_Category_can_not_create_category_with_null_name(self):
        with pytest.raises(ValueError, match="name can not be empty or null"):
            Category(name=None)

    def test_Category_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name can not be longer than 255 caracteres"):
            Category(name=self.faker.sentence(nb_words=100))