from django.urls import path

from apps.product.views import ProductRetrieveView, ProductListView, CategoryRetrieveView, CategoryListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('product/<id>/', ProductRetrieveView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<id>/', CategoryRetrieveView.as_view(), name='category-detail')
]
