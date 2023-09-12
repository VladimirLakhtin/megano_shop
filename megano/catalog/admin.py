from django.contrib import admin

from catalog.models import Category, CategoryImage
from products.models import Tag


@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    """Category image admin model"""

    list_display = ['src', 'alt']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin model"""

    list_display = ["title", "src", "image", "parent"]
    list_filter = ["title", "parent"]
    search_fields = ["title"]

    def src(self, obj):
        return obj.image.src


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin model"""

    list_display = ["name"]
    search_fields = ["name"]


