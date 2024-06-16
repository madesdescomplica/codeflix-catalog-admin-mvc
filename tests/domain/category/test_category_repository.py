from inspect import isabstract

from src.domain.category import CategoryRepository


class TestCategoryRepository:
    def test_should_CategoryRepository_is_an_abstract_class(self):
        assert isabstract(CategoryRepository)