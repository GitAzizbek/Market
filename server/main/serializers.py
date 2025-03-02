from rest_framework import serializers
from .models import ProductModel, ColorModel, SizeModel, ProductColorSizeModel, ProductImageModel

# Serializer for ColorModel
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorModel
        fields = ['id', 'name']

# Serializer for SizeModel
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeModel
        fields = ['id', 'size']

# Serializer for ProductColorSizeModel (product variants: color, size, quantity)
class ProductColorSizeSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    size = SizeSerializer()

    class Meta:
        model = ProductColorSizeModel
        fields = ['color', 'size', 'quantity']

# Serializer for ProductImageModel
class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImageModel
        fields = ['id', 'image']

    def get_image(self, obj):
        return f"api/{obj.image}"
# Serializer for ProductModel
class ProductSerializer(serializers.ModelSerializer):
    colors = ProductColorSizeSerializer(source='productcolorsizemodel_set', many=True, read_only=True)
    images = ProductImageSerializer(source='images.all', many=True, read_only=True)

    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'description', 'price', 'status', 'created_at', 'updated_at', 'colors', 'images']


# Serializer to create a product (including variants and images)
class ProductCreateSerializer(serializers.ModelSerializer):
    colors = serializers.ListField(child=serializers.JSONField(), write_only=True)
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = ProductModel
        fields = ['name', 'description', 'price', 'status', 'colors', 'images']

    def create(self, validated_data):
        colors_data = validated_data.pop('colors')
        images_data = validated_data.pop('images')

        # Create the product
        product = ProductModel.objects.create(**validated_data)

        # Create the product variants (color, size, quantity)
        for color_data in colors_data:
            color_name = color_data.get('color')
            size_list = color_data.get('sizes', [])

            color, _ = ColorModel.objects.get_or_create(name=color_name)
            product_color_size = ProductColorSizeModel.objects.create(product=product, color=color)

            for size_name in size_list:
                size, _ = SizeModel.objects.get_or_create(size=size_name)
                product_color_size.sizes.add(size)

        # Create the product images
        for image_data in images_data:
            ProductImageModel.objects.create(product=product, image=image_data)

        return product
