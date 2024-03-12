from rest_framework import serializers

from apps.product.models import Product, ProductImage, Category


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

    def get_subcategory(self, obj):
        subcategories = obj.subcategory.all().values()
        return ProductSubcategorySerializer(subcategories, many=True).data

    def get_images(self, obj):
        images = obj.product_images.all()
        return [product_image.image.url for product_image in images]


class ProductListSerializer(ProductSerializer):
    class Meta:
        model = ProductSerializer.Meta.model
        fields = ['id', 'name', 'price', 'images']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']

    @staticmethod
    def get_subcategories(obj):
        subcategories = obj.subcategories
        return SubcategorySerializer(subcategories, many=True).data


class SubcategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'products']

    @staticmethod
    def get_products(obj):
        products = obj.products.all()
        return ProductListSerializer(products, many=True).data


class ProductSubcategorySerializer(SubcategorySerializer):
    class Meta:
        model = ProductSerializer.Meta.model
        fields = ['id', 'name']
