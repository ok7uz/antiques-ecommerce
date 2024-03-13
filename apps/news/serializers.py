from django.urls import reverse
from rest_framework import serializers

from apps.news.models import News


class NewsListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'url', 'date', 'image', 'title', 'subtitle']

    def get_url(self, obj):
        return reverse('news-detail', args=[obj.id])


class NewsSerializer(NewsListSerializer):
    class Meta:
        model = NewsListSerializer.Meta.model
        fields = ['id', 'date', 'title', 'content']
