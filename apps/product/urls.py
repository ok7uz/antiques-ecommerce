from django.urls import path

from apps.product.views import ProductListView, NewProductsView, MainCategoryListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('new/', NewProductsView.as_view(), name='new-products'),
    path('<uuid:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('main_categories/', MainCategoryListView.as_view(), name='categories'),
]
