from django.contrib import admin

from infrastructure.category.models import Category


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
