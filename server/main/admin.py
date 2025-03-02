from django.contrib import admin
from .models import ProductModel, ProductColorSizeModel, SizeModel, ColorModel, ProductImageModel
from unfold.admin import ModelAdmin, TabularInline
from django.forms.models import BaseInlineFormSet

class ProductImageInline(TabularInline):
    model = ProductImageModel
    extra = 1  # Qo'shimcha rasm qo'shish uchun bo'sh joylar soni

@admin.register(ProductModel)
class ProductAdmin(ModelAdmin):
    fieldsets = (
        ("Mahsulot ma'lumotlari", {"fields": ("name", "description", "price", "status")}),
    )
    list_display = ("name", "price", "status", "get_colors_sizes_quantities")
    search_fields = ("name", "description", "price")
    list_filter = ('created_at', 'status')
    ordering = ("name", "status",)
    inlines = [ProductImageInline]  # Inline ni qo'shing

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