from django.urls import path

from apps.cart.views import CartCreateView, CartView

urlpatterns = [
    path('', CartCreateView.as_view(), name='cart'),
    path('<uuid:id>/', CartView.as_view(), name='cart-detail')
]
