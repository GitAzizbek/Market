from django.db import models
from django.contrib.auth import get_user_model
from main.models import *

User = get_user_model()

class OrderModel(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Naqd pul'),
        ('card', 'Kartadan kartaga'),
    ]
    
    DELIVERY_METHOD_CHOICES = [
        ('pickup', 'Olib ketish'),
        ('delivery', 'Pochta orqali yetkazib berish')
    ]

    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('confirmed', 'Tasdiqlangan'),
        ('canceled', 'Bekor qilingan'),
        ('delivered', 'Yetkazib berilgan'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name="To'lov usuli")
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_METHOD_CHOICES, verbose_name="Yetkazib berish usuli")
    delivery_address = models.TextField(blank=True, null=True, verbose_name="Yetkazib berish manzili")
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="To'lov holati")
    payment_check = models.FileField(upload_to="payment_checks/", blank=True, null=True, verbose_name="To'lov cheki")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Umumiy summa")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:  # Faqat mavjud buyurtmalarda tekshirish
            old_order = OrderModel.objects.get(pk=self.pk)

            if old_order.payment_status == "pending" and self.payment_status == "confirmed":
                # ✅ TASDIQLANGANDA: OMBORDAN KAMAYTIRISH VA KASSAGA QO‘SHISH
                cashbox, created = CashboxModel.objects.get_or_create(id=1)
                cashbox.total_income += self.total_amount
                cashbox.save()

            elif old_order.payment_status == "confirmed" and self.payment_status == "canceled":
                # ❌ BEKOR QILINGANDA: OMBORGA QAYTARISH VA KASSADAN AYIRISH
                cashbox = CashboxModel.objects.get(id=1)
                cashbox.total_income -= self.total_amount
                cashbox.save()

                for item in self.items.all():
                    item.variant.quantity += item.quantity
                    item.variant.save()
            elif old_order.payment_status == "canceled" and self.payment_status == "confirmed":
                # ❌ BEKOR QILINGANDA: OMBORGA QAYTARISH VA KASSADAN AYIRISH
                cashbox = CashboxModel.objects.get(id=1)
                cashbox.total_income += self.total_amount
                cashbox.save()

                for item in self.items.all():
                    item.variant.quantity -= item.quantity
                    item.variant.save()
            elif old_order.payment_status == "pending" and self.payment_status == "delivered":
                cashbox = CashboxModel.objects.get(id=1)
                cashbox.total_income += self.total_amount
                cashbox.save()
            elif old_order.payment_status == "canceled" and self.payment_status == "delivered":
                # ❌ BEKOR QILINGANDA: OMBORGA QAYTARISH VA KASSADAN AYIRISH
                cashbox = CashboxModel.objects.get(id=1)
                cashbox.total_income += self.total_amount
                cashbox.save()

                for item in self.items.all():
                    item.variant.quantity -= item.quantity
                    item.variant.save()
            elif old_order.payment_status == "delivered" and self.payment_status == "canceled":
                # ❌ BEKOR QILINGANDA: OMBORGA QAYTARISH VA KASSADAN AYIRISH
                cashbox = CashboxModel.objects.get(id=1)
                cashbox.total_income -= self.total_amount
                cashbox.save()

                for item in self.items.all():
                    item.variant.quantity += item.quantity
                    item.variant.save()
            elif old_order.payment_status == "pending" and self.payment_status == "canceled":
                for item in self.items.all():
                    item.variant.quantity += item.quantity
                    item.variant.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.user.username}"

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductColorSizeModel, on_delete=models.CASCADE, verbose_name="Mahsulot varianti")
    quantity = models.PositiveIntegerField(verbose_name="Miqdor")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narx")

    def __str__(self):
        return f"{self.variant.product.name} - {self.variant.color.name} - {self.variant.size.size}"

    class Meta:
        verbose_name = "Buyurtma Mahsuloti"
        verbose_name_plural = "Buyurtma Mahsulotlari"


class CashboxModel(models.Model):
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Umumiy daromad")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Oxirgi yangilanish")

    def __str__(self):
        return f"Kassa: {self.total_income} so'm"

    class Meta:
        verbose_name = "Kassa"
        verbose_name_plural = "Kassa"

class CommentsModel(models.Model):
    text = models.TextField()
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rate = models.IntegerField(default=1)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = "Izohlar"
        verbose_name_plural = "Izohlar"

class DeliveryMethods(models.Model):
    DELIVERY_METHODS = [
        ('active', "Faol"),
        ('disactive', 'Faolsizlantirilgan')
    ]
    
    method_name = models.CharField(max_length=500)
    img = models.ImageField(upload_to="delivery_images")
    status = models.CharField(max_length=500, choices=DELIVERY_METHODS, default="active")
    address = models.CharField(max_length=2000, blank=True, null=True)


    def __str__(self):
        return self.method_name
    
    class Meta:
        verbose_name = "Yetkazib berish turlari"
        verbose_name_plural = "Yetkazib berish turlari"

class PaymentMethods(models.Model):
    PAYMENT_METHODS = [
        ('active', "Faol"),
        ('disactive', 'Faolsizlantirilgan')
    ]

    method_name = models.CharField(max_length=1000)
    img = models.ImageField(upload_to="payment_images")
    status = models.CharField(max_length=500, choices=PAYMENT_METHODS, default="active")
    card = models.CharField(max_length=500, blank=True, null=True)
    card_holder = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.method_name
    
    class Meta:
        verbose_name = "To'lov turlari"
        verbose_name_plural = "To'lov turlari"