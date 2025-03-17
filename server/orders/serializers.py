from rest_framework import serializers
from .models import OrderModel, OrderItemModel, CommentsModel

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemModel
        fields = ['variant', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = OrderModel
        fields = ('id', 'payment_method', 'delivery_method', 'delivery_address', 'payment_check', 'total_amount', 'items', 'payment_status')

    def validate(self, data):
        if data['delivery_method'] == 'delivery' and not data.get('delivery_address'):
            raise serializers.ValidationError("Yetkazib berish uchun manzil kiritish majburiy.")
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        order = OrderModel.objects.create(**validated_data)

        total_amount = 0
        for item_data in items_data:
            variant = item_data['variant']  # ✅ `variant` obyektini olish
            if variant.quantity < item_data['quantity']:  # ✅ Stokni tekshirish
                raise serializers.ValidationError(f"{variant.product.name} - {variant.color.name} - {variant.size.size} mahsulotidan yetarli emas!")

            variant.quantity -= item_data['quantity']  # 🔻 Ombordan mahsulot kamaytirish
            variant.save()
            
            price = variant.product.price * item_data['quantity']  # ✅ Mahsulot narxini olish
            total_amount += price

            OrderItemModel.objects.create(order=order, variant=variant, quantity=item_data['quantity'], price=price)  # ✅ `price` to‘g‘ri hisoblanadi
        
        order.total_amount = total_amount
        order.save()
        return order



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsModel
        fields = '__all__'
        depth = 1