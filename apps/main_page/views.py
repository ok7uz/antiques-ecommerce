from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.main_page.models import News, Banner, Video, Expert
from apps.main_page.serializers import NewsListSerializer, NewsSerializer, BannerSerializer, VideoSerializer, \
    ExpertSerializer
from config.settings.base import EMAIL_HOST_USER, RECIPIENT_EMAIL


class NewsView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: NewsSerializer()},
        tags=['Main Page'],
    )
    def get(self, request, news_id):
        instance = get_object_or_404(News, id=news_id)
        serializer = NewsSerializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewsListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: NewsListSerializer(many=True)},
        tags=['Main Page'],
    )
    def get(self, request):
        queryset = News.objects.all()
        serializer = NewsListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BannerListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: BannerSerializer(many=True)},
        tags=['Main Page'],
    )
    def get(self, request):
        queryset = Banner.objects.all()
        serializer = BannerSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoListView(APIView):
    permission_classes = [AllowAny]
    type_param = openapi.Parameter(
        'type', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Type of video. Choices: [main, event]')

    @swagger_auto_schema(
        manual_parameters=[type_param],
        responses={200: VideoSerializer(many=True)},
        tags=['Main Page'],
    )
    def get(self, request):
        queryset = Video.objects.all()
        video_type = request.query_params.get('type', None)
        if video_type:
            queryset = queryset.filter(type=video_type)
        serializer = VideoSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpertListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: ExpertSerializer(many=True)},
        tags=['Main Page'],
    )
    def get(self, request):
        queryset = Expert.objects.all()
        serializer = ExpertSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

