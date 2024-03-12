from rest_framework import serializers

from apps.product.models import Product, ProductImage, Category


class ProductImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['url']

    @staticmethod
    def get_url(obj):
        return obj.image.url


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def get_category(obj):
        categories = obj.category.all()
        return ProductCategorySerializer(categories, many=True).data

    @staticmethod
    def get_images(obj):
        images = obj.product_images.all()
        return ProductImageSerializer(images, many=True).data


class ProductListSerializer(ProductSerializer):
    class Meta:
        model = ProductSerializer.Meta.model
        fields = ['id', 'name', 'price', 'images']


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'products']

    @staticmethod
    def get_products(obj):
        products = obj.products.all()
        return ProductSerializer(products, many=True).data
