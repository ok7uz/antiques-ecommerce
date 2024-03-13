from django.db.models import Q

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.product.models import Product, Category,  MainCategory, SubCategory
from apps.product.serializers import (
    ProductListSerializer, ProductSerializer, MainCategorySerializer, SubCategorySerializer
)


class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductView(APIView):
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


class ProductListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: ProductListSerializer(many=True)},
        tags=['Product'],
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of items per page", type=openapi.TYPE_INTEGER),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        queryset = Product.objects.all()
        search_term = request.GET.get('search')

        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) | Q(description__icontains=search_term)
            )

        paginator = Pagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductListSerializer(result_page, context={'request': request}, many=True)
        response = paginator.get_paginated_response(serializer.data)

        return Response(response.data, status=response.status_code)


class CategoryView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: MainCategorySerializer(many=True)},
        tags=['Product'],
    )
    def get(self, request, id):
        try:
            instance = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MainCategorySerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = MainCategory.objects.all()

        search_term = request.GET.get('search')
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)

        serializer = MainCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubCategoryView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: SubCategorySerializer(many=True)},
        tags=['Product'],
    )
    def get(self, request, id):
        try:
            instance = SubCategory.objects.get(id=id)
        except SubCategory.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubCategorySerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
