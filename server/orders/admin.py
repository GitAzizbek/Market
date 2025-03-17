from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import OrderModel, OrderItemModel
from unfold.admin import ModelAdmin, TabularInline
from django.utils.safestring import mark_safe
from django.utils.timezone import localtime
from .models import CashboxModel, CommentsModel


@admin.register(CommentsModel)
class ReviewAdmin(ModelAdmin):
    search_fields = ('__all__',)

@admin.register(CashboxModel)
class CashboxAdmin(ModelAdmin):
    list_display = ('total_income', 'formatted_last_updated')
    readonly_fields = ('cashbox_card', 'total_income', 'last_updated')
    list_filter = ('total_income',)  # Narx bo‘yicha filter
    
    def formatted_last_updated(self, obj):
        return localtime(obj.last_updated).strftime("%Y-%m-%d %H:%M:%S")

    formatted_last_updated.short_description = "Oxirgi yangilanish"

    def cashbox_card(self, obj):
        formatted_date = localtime(obj.last_updated).strftime("%d-%m-%Y %H:%M")
        return mark_safe(f"""
        <div style="padding:20px; background:#1e3a8a; color:#ffffff; 
                    border-radius:12px; text-align:center; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
            <h2 style="margin: 10px 0; font-size: 24px;">💰 Kassa</h2><br/>
            <p style="font-size: 22px; font-weight: bold;">{obj.total_income:,} so'm</p><br/>
            <p style="font-size: 14px; opacity: 0.8;">📅 Oxirgi yangilanish: {formatted_date}</p>
        </div>
        """)

    cashbox_card.allow_tags = True
    cashbox_card.short_description = "📌 Kassa"

    def has_add_permission(self, request):
        return not CashboxModel.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return True

class OrderItemInline(TabularInline):
    model = OrderItemModel
    extra = 0
    readonly_fields = ('get_product', 'get_color', 'get_size', 'quantity', 'price')

    def get_product(self, obj):
        return obj.variant.product.name if obj.variant else "Noma'lum"
    get_product.short_description = "Mahsulot"

    def get_color(self, obj):
        return obj.variant.color.name if obj.variant else "Noma'lum"
    get_color.short_description = "Rang"

    def get_size(self, obj):
        return obj.variant.size.size if obj.variant else "Noma'lum"
    get_size.short_description = "O‘lcham"

@admin.register(OrderModel)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'user', 'payment_method', 'payment_status', 'total_amount', 'created_at', 'get_payment_check')
    list_filter = ('payment_method', 'payment_status', 'created_at')
    search_fields = ('user__username', 'id')
    readonly_fields = ('user', 'payment_method', 'total_amount', 'created_at', 'updated_at', 'get_payment_check', 'delivery_method', 'delivery_address')
    inlines = [OrderItemInline]
    
    actions = ['confirm_order', 'cancel_order']
    
    def get_payment_check(self, obj):
        if obj.payment_check:
            return mark_safe(f'<a href="{obj.payment_check.url}" target="_blank">Chekni ko‘rish</a>')
        return "Mavjud emas"
    get_payment_check.short_description = "To‘lov Cheki"
    
    def confirm_order(self, request, queryset):
        queryset.update(payment_status='confirmed')
    confirm_order.short_description = "Buyurtmani tasdiqlash"
    
    def cancel_order(self, request, queryset):
        queryset.update(payment_status='canceled')
    cancel_order.short_description = "Buyurtmani bekor qilish"

    def has_add_permission(self, request):
        return False  # Admin panelda yangi buyurtma qo‘shish taqiqlangan

@admin.register(OrderItemModel)
class OrderItemAdmin(ModelAdmin):
    list_display = ('order', 'get_product', 'get_color', 'get_size', 'quantity', 'price')
    search_fields = ('order__id', 'variant__product__name')
    readonly_fields = ('order', 'get_product', 'get_color', 'get_size', 'quantity', 'price')

    def get_product(self, obj):
        return obj.variant.product.name if obj.variant else "Noma'lum"
    get_product.short_description = "Mahsulot"

    def get_color(self, obj):
        return obj.variant.color.name if obj.variant else "Noma'lum"
    get_color.short_description = "Rang"

    def get_size(self, obj):
        return obj.variant.size.size if obj.variant else "Noma'lum"
    get_size.short_description = "O‘lcham"

    def has_add_permission(self, request):
        return False
