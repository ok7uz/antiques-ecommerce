from django.urls import path

from apps.news.views import NewsListView, NewsView

urlpatterns = [
    path('', NewsListView.as_view(), name='news'),
    path('<uuid:id>/', NewsView.as_view(), name='news-detail')
]
