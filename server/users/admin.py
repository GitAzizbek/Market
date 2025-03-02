from django.contrib import admin
from django.contrib.auth.models import Group
from .models import UserModel, DistrictModel, CityModel
from unfold.admin import ModelAdmin

admin.site.site_header = "Mening Admin Panelim"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Boshqaruv paneliga xush kelibsiz!"

admin.site.unregister(Group)

@admin.register(UserModel)
class CustomUserAdmin(ModelAdmin):
    fieldsets = (
        (None, {"fields": ("phone",)}),
        ("Shaxsiy ma'lumotlar", {"fields": ("first_name", "telegram_id", "avatar", "address", "district", "city", "longt", "lat")}),
        ("Vaqt belgilari", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "password1", "password2"),
        }),
    )
    list_display = ("phone", "first_name", "is_active", "is_staff")
    search_fields = ("phone", "first_name")
    ordering = ("phone",)

@admin.register(DistrictModel)
class CustomDistrictAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(CityModel)
class CustomCityAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
