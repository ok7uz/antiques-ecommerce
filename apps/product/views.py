from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.product.models import Product, Category
from apps.product.serializers import ProductRetrieveSerializer, ProductListSerializer, CategoryRetrieveSerializer, \
    CategoryListSerializer


class ProductRetrieveView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a product",
        tags=['Product'],
        responses={200: ProductRetrieveSerializer()}
    )
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductRetrieveSerializer(product)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a product",
        tags=['Product'],
        responses={200: ProductListSerializer()}
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products)
        print(serializer.data)
        data = serializer.data
        return Response(data['products'], status=status.HTTP_200_OK)


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
