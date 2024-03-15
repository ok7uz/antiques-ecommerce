from django.db.models import Q
from django.http import JsonResponse

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.product.models import Product, Category,  MainCategory
from apps.product.serializers import (
    ProductListSerializer, ProductSerializer, MainCategorySerializer
)


class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: ProductListSerializer()},
        tags=['Product'],
    )
    def get(self, request):
        queryset = Product.objects.all()

        data = request.query_params
        category = data.get('category', None)

        if category:
            queryset = queryset.filter(
                Q(category__id=category) | Q(category__parent__id=category) | Q(category__parent__parent__id=category)
            )

        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: ProductSerializer()},
        tags=['Product'],
    )
    def get(self, request, id):
        try:
            instance = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(instance, context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewProductsView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: ProductListSerializer(many=True)},
        tags=['Product'],
    )
    def get(self, request):
        queryset = Product.new_products.all().order_by('-created')
        serializer = ProductListSerializer(queryset, context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MainCategoryListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: MainCategorySerializer(many=True)},
        tags=['Product'],
    )
    def get(self, request):
        queryset = MainCategory.objects.all()
        serializer = MainCategorySerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def custom404(request, exception=None):
    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    })
