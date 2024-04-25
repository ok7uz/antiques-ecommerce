from rest_framework import serializers

from apps.main_page.models import News, Banner, Video, Expert


class NewsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ['id', 'date', 'image', 'title', 'content']


class NewsSerializer(NewsListSerializer):

    class Meta:
        model = NewsListSerializer.Meta.model
        fields = ['id', 'date', 'image', 'title', 'content']


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ['title', 'subtitle', 'image', 'has_button', 'button_url']


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ['title', 'type', 'url', 'banner']


class ExpertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expert
        fields = ['name', 'about', 'image']
