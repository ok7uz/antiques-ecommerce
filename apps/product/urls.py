from django.urls import path

from apps.product.views import ProductView, NewProductsView, CategoryView, CategoryListView, custom404

urlpatterns = [
    path('new/', NewProductsView.as_view(), name='new-products'),
    path('<uuid:id>/', ProductView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<uuid:id>/', CategoryView.as_view(), name='category-detail'),
]
