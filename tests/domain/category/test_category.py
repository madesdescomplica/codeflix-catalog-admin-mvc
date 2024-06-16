from uuid import uuid4
from faker import Faker
import pytest

from src.domain.category import Category


class TestCategory:
    faker = Faker()
    category_id = uuid4()
    name = faker.word()
    description = faker.sentence()

    def test_Category_must_have_the_required_name(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

    def test_Category_can_not_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name can not be empty or null"):
            Category(name="")

    def test_Category_can_not_create_category_with_null_name(self):
        with pytest.raises(ValueError, match="name can not be empty or null"):
            Category(name=None)