from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone must be provided')
        extra_fields.setdefault('is_active', True)
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone must be provided')

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(phone, password, **extra_fields)

class DistrictModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyat"

class CityModel(models.Model):
    name = models.CharField(max_length=255)
    district = models.ForeignKey(DistrictModel, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Shaxar"
        verbose_name_plural = "Shaxar"

class UserModel(AbstractUser):
    username = None  # AbstractUser'dan keladigan username maydonini olib tashlash
    phone = models.CharField(max_length=20, unique=True, verbose_name="Telefon raqami")
    telegram_id = models.CharField(max_length=30, verbose_name="Telegram id raqami")
    first_name = models.CharField(max_length=500, blank=True, null=True, verbose_name="FIO")
    avatar = models.ImageField(upload_to="media/avatars", blank=True, verbose_name="Rasmi")
    district = models.ForeignKey(DistrictModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Viloyat")
    city = models.ForeignKey(CityModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Shaxar")
    address = models.CharField(max_length=600, blank=True, null=True, verbose_name="Manzil")
    longt = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ['telegram_id', 'first_name']

    def __str__(self) -> str:
        return self.phone

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
