from django.http import JsonResponse
from drf_yasg import openapi
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from apps.product.models import Product, Category
from apps.product.serializers import ProductListSerializer, ProductSerializer, CategoryDetailSerializer


class ProductListView(APIView):
    permission_classes = [AllowAny]
    category_id_param = openapi.Parameter(
        'category_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='(sub)category id')
    sidebar_id_param = openapi.Parameter(
        'sidebar_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='sidebar (sub)category id')
    page_param = openapi.Parameter(
        'page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='page number')
    search_param = openapi.Parameter(
        'search', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='searching')

    def get_queryset(self):
        queryset = Product.objects.all()
        data = self.request.query_params
        category_id = data.get('category_id', None)
        sidebar_id = data.get('sidebar_id', None)
        search = data.get('search', None)

        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if sidebar_id:
            queryset = queryset.filter(category__id=sidebar_id)
        if search:
            search_conditions = Q()
            search_conditions |= Q(name__icontains=search)
            search_conditions |= Q(category__name__icontains=search)
            search_conditions |= Q(category__parent__name__icontains=search)
            search_conditions |= Q(description__icontains=search)
            search_conditions |= Q(vendor_code__icontains=search)
            search_conditions |= Q(history__icontains=search)
            search_conditions |= Q(characteristic__icontains=search)
            search_conditions |= Q(size__icontains=search)
            queryset = queryset.filter(search_conditions).distinct()
        
        queryset = queryset.prefetch_related('category', 'category__parent')
        return queryset

    @swagger_auto_schema(
        manual_parameters=[category_id_param, sidebar_id_param, page_param, search_param],
        responses={200: ProductListSerializer(many=True)},
        pagination_class=PageNumberPagination,
        tags=['Product'],
    )
    def get(self, request):
        pagination = PageNumberPagination()
        pagination.page_size = 9
        queryset = self.get_queryset()
        page = pagination.paginate_queryset(queryset, request)
        serializer = ProductListSerializer(page, many=True, context={'request': request})
        return pagination.get_paginated_response(serializer.data)


class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: ProductSerializer()},
        tags=['Product'],
    )
    def get(self, request, product_id):
        try:
            instance = Product.objects.get(id=product_id)
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
        'error': 'Not found'
    })
