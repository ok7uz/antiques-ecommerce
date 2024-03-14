from django.urls import reverse
from rest_framework import serializers

from apps.product.models import Product, ProductImage, Category, MainCategory, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products']

    def get_products(self, obj):
        products = obj.products.all()
        return ProductListSerializer(products, many=True).data


class MainCategorySerializer(serializers.ModelSerializer):
    children = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'children']


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_images(self, obj):
        images = obj.images.all()
        return [image.image.url for image in images]


class ProductListSerializer(ProductSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductSerializer.Meta.model
        fields = ['id', 'name', 'url', 'price', 'images']

    def get_url(self, obj):
        return reverse('product-detail', args=[obj.id])
