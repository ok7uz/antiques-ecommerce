from django.urls import reverse
from rest_framework import serializers

from apps.product.models import Product, ProductImage, Category, MainCategory, SubCategory


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class SubCategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products']

    def get_products(self, obj):
        products = obj.products.all()
        return ProductListSerializer(products, many=True).data


class MainCategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_categories', 'images']

    def get_sub_categories(self, obj):
        print(obj)
        return None


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = MainCategorySerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(ProductSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductSerializer.Meta.model
        fields = ['id', 'name', 'url', 'price', 'images']

    def get_url(self, obj):
        return reverse('product-detail', args=[obj.id])




# class SubcategorySerializer(serializers.ModelSerializer):
#     products = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = Subcategory
#         fields = ['id', 'name', 'products']
#
#     def get_products(self, obj):
#         products = obj.products.all()
#         return ProductListSerializer(products, many=True).data
