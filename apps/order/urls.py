from django.urls import path

from apps.order.views import OrderView, CallbackView

urlpatterns = [
    path('order/', OrderView.as_view(), name='order-create'),
    path('callback/', CallbackView.as_view(), name='callback'),
]
