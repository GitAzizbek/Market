from rest_framework import serializers
from .models import ProductModel, ColorModel, SizeModel, ProductColorSizeModel

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorModel
        fields = ['id', 'name']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeModel
        fields = ['id', 'size']

class ProductColorSizeSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    size = SizeSerializer()

    class Meta:
        model = ProductColorSizeModel
        fields = ['color', 'size', 'quantity']

class ProductSerializer(serializers.ModelSerializer):
    colors = ProductColorSizeSerializer(source='productcolorsizemodel_set', many=True, read_only=True)

    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'description', 'price', 'image', 'status', 'colors']


class ProductCreateSerializer(serializers.ModelSerializer):
    colors = serializers.ListField(child=serializers.JSONField(), write_only=True)

    class Meta:
        model = ProductModel
        fields = ['name', 'description', 'price', 'quantity', 'image', 'status', 'colors']

    def create(self, validated_data):
        colors_data = validated_data.pop('colors')
        product = ProductModel.objects.create(**validated_data)

        for color_data in colors_data:
            color_name = color_data.get('color')
            size_list = color_data.get('sizes', [])

            color, _ = ColorModel.objects.get_or_create(name=color_name)
            product_color_size = ProductColorSizeModel.objects.create(product=product, color=color)

            for size_name in size_list:
                size, _ = SizeModel.objects.get_or_create(size=size_name)
                product_color_size.sizes.add(size)

        return product
