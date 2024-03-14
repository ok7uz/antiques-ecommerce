from django.urls import reverse
from rest_framework import serializers
from django.core.exceptions import ValidationError

from apps.product.models import Product, ProductImage, Category, MainCategory, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class MainCategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'products', 'sub_categories']

    def get_products(self, obj):
        get_data = self.context['request'].query_params
        subcategory = get_data.get('subcategory', None)
        products = Product.objects.filter(category__parent=obj)

        if subcategory:
            try:
                products = products.filter(category_id=subcategory)
            except ValidationError:
                products = []

        return ProductListSerializer(products, many=True).data


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
