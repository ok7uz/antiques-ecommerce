from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.product.models import Product, Category
from apps.product.serializers import ProductListSerializer, CategoryRetrieveSerializer, \
    CategoryListSerializer, ProductSerializer


class Pagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductRetrieveView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a product",
        tags=['Product'],
        responses={200: ProductSerializer()}
    )
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(ListAPIView):
    # swagger_schema = {'tags': ['Product']}
    permission_classes = [AllowAny]
    pagination_class = Pagination
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryRetrieveView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a category",
        tags=['Product'],
        responses={200: CategoryRetrieveSerializer()}
    )
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
            serializer = CategoryRetrieveSerializer(category)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(APIView):
    permission_classes = [AllowAny]
    pagination_class = Pagination

    @swagger_auto_schema(
        operation_description="Categories",
        tags=['Product'],
        responses={200: CategoryListSerializer()}
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories)
        data = serializer.data
        return Response(data['categories'], status=status.HTTP_200_OK)
