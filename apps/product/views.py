from django.db.models import Q
from django.http import JsonResponse
from drf_yasg import openapi

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from apps.product.models import Product, Category
from apps.product.serializers import (
    ProductListSerializer, ProductSerializer, CategorySerializer, CategoryDetailSerializer
)



class ProductListView(APIView):
    permission_classes = [AllowAny]
    category_id_param = openapi.Parameter(
        'category_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='(sub)category id')
    left_category_id_param = openapi.Parameter(
        'left_category_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='left (sub)category id')

    def get_queryset(self):
        queryset = Product.objects.all()
        data = self.request.query_params
        category_id = data.get('category_id', None)
        sidebar_id = data.get('sidebar_id', None)

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        if sidebar_id:
            queryset = queryset.filter(category__id=sidebar_id)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[category_id_param, left_category_id_param],
        responses={200: ProductListSerializer(many=True)},
        tags=['Product'],
    )
    def get(self, request):
        queryset = self.get_queryset()
        print(queryset)
        serializer = ProductListSerializer(queryset, many=True, context={'request': request})
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
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(instance, context={'request': request})
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


class CategoryListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: CategorySerializer(many=True)},
        tags=['Category'],
    )
    def get(self, request):
        queryset = Category.objects.filter(is_top=True)
        serializer = CategorySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: CategoryDetailSerializer()},
        tags=['Category'],
    )
    def get(self, request, category_id):
        queryset = Category.objects.filter(is_top=True)
        try:
            category = queryset.get(id=category_id)
            serializer = CategoryDetailSerializer(category, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except queryset.model.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


def custom404(request, exception=None):
    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    })
