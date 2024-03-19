from django.urls import path

from apps.product.views import ProductListView, NewProductsView, ProductDetailView, CategoryListView, CategoryView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('new/', NewProductsView.as_view(), name='new-products'),
    path('<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:category_id>/', CategoryView.as_view(), name='category-detail'),
]
