from django.urls import reverse
from rest_framework import serializers

from apps.product.models import Product, Category, MainCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_categories']

    def get_sub_categories(self, obj):
        return SubCategorySerializer(obj.sub_categories, many=True).data


class MainCategorySerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'image', 'categories']

    def get_categories(self, obj):
        return CategorySerializer(obj.sub_categories, many=True).data


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
