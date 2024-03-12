from django.urls import path

from apps.product.views import ProductView, ProductListView, CategoryView, CategoryListView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('<uuid:product_id>/', ProductView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<uuid:category_id>/', CategoryView.as_view(), name='category-detail')
]
