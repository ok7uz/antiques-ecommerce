from rest_framework import serializers

from apps.main_page.models import News, Banner, Video


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['slug', 'date', 'image', 'title', 'content']


class NewsSerializer(NewsListSerializer):
    class Meta:
        model = NewsListSerializer.Meta.model
        fields = ['slug', 'date', 'image', 'title', 'content']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['title', 'subtitle', 'image']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'url', 'banner']
