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
        fields = [
            'name', 'price', 'vendor_code', 'history', 'characteristic',
            'size', 'images', 'video_url', 'description'
        ]

    @swagger_serializer_method(serializers.ListField(child=serializers.URLField()))
    def get_images(self, obj):
        request = self.context['request']
        build_uri = request.build_absolute_uri
        images = obj.images.all()
        return [build_uri(image.image.url) for image in images]


class ProductListSerializer(ProductSerializer):
    catalog = serializers.SerializerMethodField()

    class Meta:
        model = ProductSerializer.Meta.model
        fields = ['id', 'name', 'catalog', 'price', 'images']

    def get_catalog(self, obj):
        category = obj.category.filter(is_top=True).first()
        return category.name if category else None


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
    sidebar = serializers.SerializerMethodField()

    @swagger_serializer_method(CategorySerializer(many=True))
    def get_sidebar(self, obj):
        return CategorySerializer(Category.objects.filter(is_left=True), many=True).data
