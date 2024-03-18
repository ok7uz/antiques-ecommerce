from rest_framework import serializers

from apps.order.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_email', 'customer_address', 'items', 'total_price']

    def create(self, validated_data):
        data = validated_data
        items = data['items']

        order = Order.objects.create(
            customer_name=validated_data['customer_name'],
            customer_phone=validated_data['customer_phone'],
            customer_email=validated_data['customer_email'],
            customer_address=validated_data['customer_address'],
            total_price=validated_data['total_price']
        )

        for item in items:
            order.items.add(item['product'])

        order.save()

        return order
