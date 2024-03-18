from django.urls import path

from apps.order.views import OrderView

urlpatterns = [
    path('', OrderView.as_view(), name='orders')
]
