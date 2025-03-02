from django.contrib import admin
from .models import ProductModel, ProductColorSizeModel, SizeModel, ColorModel
from unfold.admin import ModelAdmin
from django.forms.models import BaseInlineFormSet


@admin.register(ProductModel)
class ProductAdmin(ModelAdmin):
    fieldsets = (
        ("Mahsulot ma'lumotlari", {"fields": ("name", "description", "price", "image", "status")}),
    )
    list_display = ("name", "price", "status", "get_colors_sizes_quantities")
    search_fields = ("name", "description", "price")
    list_filter = ('created_at', 'status')
    ordering = ("name", "status",)

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
