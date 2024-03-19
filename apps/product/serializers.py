from django.urls import reverse
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.product.models import Product, Category, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    @swagger_serializer_method(serializers.ListField(child=serializers.URLField()))
    def get_images(self, obj):
        request = self.context['request']
        build_uri = request.build_absolute_uri
        images = obj.images.all()
        return [build_uri(image.image.url) for image in images]


class ProductListSerializer(ProductSerializer):
    class Meta:
        model = ProductSerializer.Meta.model
        fields = ['id', 'name', 'price', 'images']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_categories']


class CategoryDetailSerializer(serializers.Serializer):
    sub_categories = SubCategorySerializer(many=True)
    products = ProductListSerializer(many=True)
    left_menu = serializers.SerializerMethodField()

    @swagger_serializer_method(CategorySerializer(many=True))
    def get_left_menu(self, obj):
        return CategorySerializer(Category.objects.filter(left_menu=True), many=True).data

