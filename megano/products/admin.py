from django.contrib import admin

from products.models import Product, ProductImage, Review, ProductSpecification, Sale


class ProductImageInline(admin.StackedInline):
    """Product image inline model"""

    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin model"""

    inlines = ProductImageInline,

    list_display = [
        'id',
        'title',
        'price',
        'salePrice',
        'count',
        'category',
        'freeDelivery',
        "is_limited",
        "sort_index",
        "rating",
    ]
    list_filter = [
        "category",
        "freeDelivery",
        "sort_index",
    ]
    search_fields = ["title", 'fullDescription', 'description']

    def rating(self, obj: Product) -> float:
        return obj.rating

    def salePrice(self, obj: Product) -> float:
        return obj.salePrice or obj.price


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Product review admin model"""

    list_display = 'author', 'text', 'rate', 'date', 'product'
    search_fields = 'text',
    list_filter = 'author', 'date', 'product', 'rate'


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    """Product specification admin model"""

    list_display = "name", "value", "product"
    search_fields = "name",
    list_filter = "product",


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """Product sale admin model"""

    list_display = "product", "sale", "dateTo", "dateFrom", "salePrice"
    list_filter = "dateTo", "dateFrom", 'sale'
    search_fields = "product",

    def salePrice(self, obj: Sale) -> float:
        return obj.product.price * (1 - obj.sale)
