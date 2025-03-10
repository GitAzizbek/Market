from django.db import models


class CategoryModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Katalog nomi")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kataloglar"
        verbose_name_plural = "Kataloglar"
    

class ColorModel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Rang"
        verbose_name_plural = "Ranglar"

class SizeModel(models.Model):
    size = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.size
    
    class Meta:
        verbose_name = "O'lcham"
        verbose_name_plural = "O'lchamlar"

class ProductModel(models.Model):
    STATUS_CHOICES = [
        ('available', 'Mavjud'),
        ('out_of_stock', 'Tugagan'),
        ('coming_soon', 'Yaqinda keladi'),
    ]

    name = models.CharField(max_length=255, verbose_name="Maxsulot nomi")
    category = models.ManyToManyField(CategoryModel)
    description = models.TextField(blank=True, null=True, verbose_name="Maxsulot haqida")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maxsulot narxi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

class ProductColorSizeModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    color = models.ForeignKey(ColorModel, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size.size}"

    class Meta:
        verbose_name = "Mahsulot Varianti"
        verbose_name_plural = "Mahsulot Variantlari"
        unique_together = ('product', 'color', 'size')  # ✅ Bir xil mahsulot-rang-o‘lcham kombinatsiyasi takrorlanmasligi kerak

class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="products/", verbose_name="Maxsulot rasmi")

    def __str__(self):
        return f"{self.product.name} - {self.image.name}"

    class Meta:
        verbose_name = "Mahsulot Rasmi"
        verbose_name_plural = "Mahsulot Rasmlari"

class ProductReviewModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey("users.UserModel", on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    start_count = models.IntegerField(default=0)

    def __str__(self):
        return self.review[0:150]
    
    class Meta:
        verbose_name = "Izohlar"
        verbose_name_plural = "Izohlar"

class AnnounceModel(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    img = models.ImageField(upload_to="announcements")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Elonlar"
        verbose_name_plural = "Elonlar"