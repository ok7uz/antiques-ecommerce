from rest_framework import serializers
from apps.cart.models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        cart_item = CartItem(**validated_data)
        cart_item.save()
        return cart_item

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']
        extra_kwargs = {'quantity': {'required': True}}
        required_fields = ['product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = serializers.JSONField(required=True)

    def create(self, validated_data):
        items = validated_data.pop('items', None)
        cart = Cart(amount=validated_data.pop('amount'))
        cart.save()

        if not items:
            raise serializers.ValidationError({
                'items': ['This field is required and cannot be empty.']
            })

        for item in items:
            item['product'] = item.pop('product_id', None)

            serializer = CartItemSerializer(data=item)
            if serializer.is_valid():
                serializer.validated_data['cart_id'] = cart.id
                serializer.save()
            else:
                cart.delete()
                raise serializers.ValidationError(serializer.errors)

        return cart

    class Meta:
        model = Cart
        fields = ['id', 'items', 'amount']

    def get_items(self, obj):
        return CartItemSerializer(obj.items.all(), many=True).data
