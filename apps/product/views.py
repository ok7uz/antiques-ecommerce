from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from rest_framework.views import APIView

from apps.product.models import Product, Category
from apps.product.serializers import ProductListSerializer, ProductSerializer, CategorySerializer


class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductView(APIView):
    permission_classes = (AllowAny, )

    @swagger_auto_schema(
        responses={200: ProductSerializer()},
        tags=['Product'],
    )
    def get(self, request, product_id):
        try:
            instance = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListView(APIView):
    permission_classes = (AllowAny, )

    @swagger_auto_schema(
        responses={200: ProductListSerializer(many=True)},
        tags=['Product'],
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of items per page",
                              type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request):
        queryset = Product.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductListSerializer(result_page, many=True)
        response = paginator.get_paginated_response(serializer.data)

        return Response(response.data, status=response.status_code)


class CategoryView(APIView):
    permission_classes = (AllowAny, )

    @swagger_auto_schema(
        responses={200: CategorySerializer(many=True)},
        tags=['Product'],
    )
    def get(self, request, category_id):
        try:
            instance = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryListView(APIView):
    permission_classes = (AllowAny, )

    @swagger_auto_schema(
        responses={200: CategorySerializer(many=True)},
        tags=['Product'],
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of items per page",
                              type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request):
        queryset = Category.objects.all()
        paginator = Pagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CategorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
