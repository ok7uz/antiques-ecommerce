from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.order.models import Order
from apps.product.models import Product


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_email', 'customer_address', 'total_price', 'products']

    @swagger_serializer_method(serializers.ListField(child=serializers.UUIDField()))
    def get_products(self):
        return self.products

    def set_products(self):
        self.products = Product.objects.all()
        return self.products

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
