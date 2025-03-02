from django.contrib import admin
from .models import ProductModel, ProductColorSizeModel, SizeModel, ColorModel, ProductImageModel, CategoryModel, ProductReviewModel, AnnounceModel
from unfold.admin import ModelAdmin, TabularInline
from django.forms.models import BaseInlineFormSet

class ProductImageInline(TabularInline):
    model = ProductImageModel
    extra = 1  # Add 1 extra image slot for each product
    fields = ('image',)  # You can specify which fields to show in the inline form


@admin.register(ProductModel)
class ProductAdmin(ModelAdmin):
    fieldsets = (
        ("Mahsulot ma'lumotlari", {"fields": ("name", "description", "price", "status", 'category')}),
    )
    list_display = ("name", "price", "status", "get_categories", "get_colors_sizes_quantities")
    search_fields = ("name", "description", "price", "category__name")  # Searching by category name
    list_filter = ('created_at', 'status', "category",)
    ordering = ("name", "status", "category",)
    inlines = [ProductImageInline]  # Inline for product images

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    get_categories.short_description = "Kategoriya(lar)"

    def get_colors_sizes_quantities(self, obj):
        return ", ".join([f"{item.color.name} - {item.size.size} - {item.quantity}" for item in obj.productcolorsizemodel_set.all()])
    get_colors_sizes_quantities.short_description = "Ranglar, O'lchamlar va Miqdorlar"


@admin.register(SizeModel)
class SizeAdmin(ModelAdmin):
    search_fields = ("size",)


@admin.register(ColorModel)
class ColorAdmin(ModelAdmin):
    search_fields = ("name",)


@admin.register(ProductColorSizeModel)
class ProductColorSizeAdmin(ModelAdmin):
    list_display = ("product", "color", "size", "quantity")
    list_filter = ("product", "color", "size")


@admin.register(CategoryModel)
class CategoryAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ProductReviewModel)
class ReviewAdmin(ModelAdmin):
    search_fields = ('__all__',)


@admin.register(AnnounceModel)
class AnnounceAdmin(ModelAdmin):
    search_fields = ('__all__',)