from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.product.models import Filter, Product, Category, SubCategory


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'vendor_code', 'history',
            'characteristic', 'size', 'images', 'video_url', 'description'
        ]

    @swagger_serializer_method(serializers.ListField(child=serializers.URLField()))
    def get_images(self, obj):
        request = self.context['request']
        build_uri = request.build_absolute_uri
        images = obj.images.all().order_by('id')
        return [build_uri(image.image.url) for image in images]


class ProductListSerializer(ProductSerializer):
    catalog = serializers.SerializerMethodField()

    class Meta:
        model = ProductSerializer.Meta.model
        fields = ['id', 'name', 'catalog', 'price', 'images']

    def get_catalog(self, obj):
        category = obj.categories.filter(is_top=True).first()
        return category.name if category else None


class L3CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'title', 'description', 'image']


class SubCategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'title', 'image', 'description', 'subcategories']

    @swagger_serializer_method(L3CategorySerializer(many=True))
    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        return L3CategorySerializer(subcategories, many=True, context=self.context).data


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'title', 'image', 'description', 'subcategories']

    @swagger_serializer_method(SubCategorySerializer(many=True))
    def get_subcategories(self, obj):
        category_id = self.context.get('category_id', None)
        subcategories = obj.subcategories.select_related('parent').all().order_by('name')
        if category_id:  # get the sidebar subcategories corresponding to the category
            subcategories = subcategories.filter(products__categories=category_id).distinct()
        return SubCategorySerializer(subcategories, many=True, context=self.context).data


class SidebarSerializer(serializers.Serializer):
    data = serializers.SerializerMethodField()

    @swagger_serializer_method(CategorySerializer(many=True))
    def get_data(self, obj):
        category_id = obj.id
        queryset = Category.objects.filter(is_left=True, products__categories=category_id).distinct().order_by('id')
        return CategorySerializer(queryset, many=True,
                                  context={'category_id': category_id, 'request': self.context.get('request')}).data


class FilterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Filter
        fields = ('id', 'name')
    