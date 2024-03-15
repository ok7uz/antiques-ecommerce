from django.urls import reverse
from rest_framework import serializers

from apps.main_page.models import News, Banner, Video


class NewsListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'url', 'date', 'image', 'title']

    def get_url(self, obj):
        return reverse('news-detail', args=[obj.id])


class NewsSerializer(NewsListSerializer):
    class Meta:
        model = NewsListSerializer.Meta.model
        fields = ['id', 'date', 'title', 'content']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['title', 'subtitle', 'image']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['name', 'url']
