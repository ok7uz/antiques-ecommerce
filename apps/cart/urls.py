from django.urls import path

from apps.cart.views import CartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
]
