from django.urls import reverse
from rest_framework import serializers

from apps.product.models import Product, ProductImage, Category, Subcategory


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    subcategory = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_images(self, obj):
        images = obj.images.all()
        return list([product_image.image.url for product_image in images])

    def get_subcategory(self, obj):
        return {
            'id': obj.subcategory.id,
            'name': obj.subcategory.name,
        }


class ProductListSerializer(ProductSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductSerializer.Meta.model
        fields = ['id', 'name', 'url', 'price', 'images']

    def get_url(self, obj):
        return reverse('product-detail', args=[obj.id])


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']

    def get_subcategories(self, obj):
        subcategories = obj.subcategories
        return SubcategorySerializer(subcategories, many=True).data


class SubcategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'products']

    def get_products(self, obj):
        products = obj.products.all()
        return ProductListSerializer(products, many=True).data
