from uuid import UUID, uuid4

from faker import Faker
import pytest

from domain.category import Category


class TestCategory:
    faker = Faker()
    category_id = uuid4()
    name = faker.word()
    description = faker.sentence()
    is_active = faker.boolean()

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

    def test_Category_is_created_with_default_values(self):
        category = Category(name=self.name)

        assert category.name == self.name
        assert category.description == ""
        assert category.is_active is True

    def test_Category_is_created_as_active_by_default(self):
        category = Category(name=self.name)

        assert category.is_active is True

    def test_category_is_created_with_provided_values(self):
        category = Category(
            id=self.category_id,
            name=self.name,
            description=self.description,
            is_active=self.is_active
        )

        assert category.id == self.category_id
        assert category.name == self.name
        assert category.description == self.description
        assert category.is_active is self.is_active

    def test_Category_return_the_response_of__str__method(self):
        category = Category(
            id=self.category_id,
            name=self.name,
            description=self.description,
            is_active=self.is_active
        )

        assert str(category) == f"id: {self.category_id}, \
            name: {self.name}, \
            description: {self.description}, \
            is_active: {self.is_active}"

    def test_Category_return_the_response_of__repr__method(self):
        category = Category(
            id=self.category_id,
            name=self.name,
            description=self.description,
            is_active=self.is_active
        )

        assert category.__repr__() == f"id: {self.category_id}, \
            name: {self.name}, \
            description: {self.description}, \
            is_active: {self.is_active}"

class TestUpdateCategory:
    faker = Faker()
    name = faker.word()
    description = faker.sentence()

    def test_Category_update_name(self):
        updated_name = self.faker.word()
        category = Category(name=self.name, description=self.description)

        category.update_category(name=updated_name, description=self.description)

        assert category.name == updated_name
        assert category.description == self.description

    def test_Category_update_description(self):
        updated_description = self.faker.sentence()
        category = Category(name=self.name, description=self.description)

        category.update_category(name=self.name, description=updated_description)

        assert category.name == self.name
        assert category.description == updated_description

    def test_Category_update_name_and_description(self):
        updated_name = self.faker.word()
        updated_description = self.faker.sentence()
        category = Category(name=self.name, description=self.description)

        category.update_category(name=updated_name, description=updated_description)

        assert category.name == updated_name
        assert category.description == updated_description

    def test_Category_raise_exception_with_invalid_name(self):
        category = Category(name=self.name, description=self.description)

        with pytest.raises(ValueError, match="name can not be longer than 255 caracteres"):
            category.update_category(
                name=self.faker.sentence(nb_words=100),
                description=self.faker.sentence()
            )

    def test_Category_raise_exception_with_empty_name(self):
        category = Category(name=self.name, description=self.description)

        with pytest.raises(ValueError, match="name can not be empty or null"):
            category.update_category(
                name="",
                description=self.faker.sentence()
            )

    def test_Category_raise_exception_with_null_name(self):
        category = Category(name=self.name, description=self.description)

        with pytest.raises(ValueError, match="name can not be empty or null"):
            category.update_category(
                name=None,
                description=self.faker.sentence()
            )

class TestActivateCategory:
    faker = Faker()
    name = faker.word()
    description = faker.sentence()

    def test_activate_an_inactive_Category(self):
        category = Category(
            name=self.name,
            description=self.description,
            is_active=False)

        category.activate()

        assert category.is_active is True

    def test_activate_an_active_Category(self):
        category = Category(
            name=self.name,
            description=self.description,
            is_active=True)

        category.activate()

        assert category.is_active is True

    def test_deactivate_an_inactive_Category(self):
        category = Category(
            name=self.name,
            description=self.description,
            is_active=False)

        category.deactivate()

        assert category.is_active is False

    def test_deactivate_an_active_Category(self):
        category = Category(
            name=self.name,
            description=self.description,
            is_active=True)

        category.deactivate()

        assert category.is_active is False

class TestEquality:
    faker = Faker()

    def test_when_categories_have_same_id_they_are_equal(self):
        category_id = uuid4()
        category1 = Category(id=category_id, name="category1")
        category2 = Category(id=category_id, name="category1")

        assert category1 == category2

    def test_Category_equality_of_different_classes(self):
        class Dummy:
            pass

        common_id = uuid4()
        category = Category(id=common_id, name=self.faker.word())
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy