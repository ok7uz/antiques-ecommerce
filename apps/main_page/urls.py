from django.urls import path

from apps.main_page.views import NewsListView, NewsView, BannerListView, VideoListView, ExpertListView

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news'),
    path('news/<uuid:news_id>/', NewsView.as_view(), name='news-detail'),
    path('banners/', BannerListView.as_view(), name='banners'),
    path('videos/', VideoListView.as_view(), name='videos'),
    path('experts/', ExpertListView.as_view(), name='experts'),
]
