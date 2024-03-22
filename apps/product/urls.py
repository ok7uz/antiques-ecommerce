from django.urls import path

from apps.product.views import ProductListView, NewProductsView, ProductDetailView, CategoryView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('new/', NewProductsView.as_view(), name='new-products'),
    path('<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/<int:category_id>/', CategoryView.as_view(), name='category-detail'),
]
