from django.contrib import admin

from infrastructure.category.models import CategoryModel


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(CategoryModel, CategoryAdmin)
