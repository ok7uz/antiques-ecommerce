from rest_framework import serializers

from apps.order.models import Order, Callback
from apps.product.models import Product


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.ListField(
        child=serializers.IntegerField(label='id', help_text='Product ID'),
        write_only=True,
        label='Products', help_text='Order Products'
    )

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_email', 'customer_address', 'total_price', 'products']

    def create(self, validated_data):
        data = validated_data
        products = data['products']

        if not products:
            raise serializers.ValidationError({'error': 'There must be products in the order'})

        order = Order.objects.create(
            customer_name=validated_data['customer_name'],
            customer_phone=validated_data['customer_phone'],
            customer_email=validated_data['customer_email'],
            customer_address=validated_data['customer_address'],
            total_price=validated_data['total_price']
        )

        for product_id in products:
            try:
                product = Product.objects.get(id=product_id)
                order.items.add(product)
            except Product.DoesNotExist:
                order.delete()
                raise serializers.ValidationError({'error': f'Product #{product_id} not found'})
        return order


class CallbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Callback
        fields = ['applicant_name', 'applicant_email']
