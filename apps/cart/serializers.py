from rest_framework import serializers
from apps.cart.models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        cart_item = CartItem(**validated_data)
        cart_item.save()
        return cart_item

    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity']
        extra_kwargs = {'quantity': {'required': True}}
        required_fields = ['cart', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = serializers.JSONField(required=True)

    def create(self, validated_data):
        items = validated_data.pop('items', None)
        cart = Cart(amount=validated_data.pop('amount'))
        cart.save()

        for item in items:
            item['cart'] = cart.id
            item['product'] = item.pop('product_id', None)
            serializer = CartItemSerializer(data=item,)
            if serializer.is_valid():
                serializer.save()
            else:
                cart.delete()
                raise serializers.ValidationError(serializer.errors)

        return cart

    class Meta:
        model = Cart
        fields = '__all__'

    @staticmethod
    def get_items(obj):
        return CartItemSerializer(obj.items.all(), many=True).data
