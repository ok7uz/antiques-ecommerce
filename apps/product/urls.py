from django.urls import path, include

from apps.product.views import ProductListView, NewProductsView, ProductDetailView, SidebarView, CategoryView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('new-products/', NewProductsView.as_view(), name='new-products'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/<int:category_id>/', include([
        path('', CategoryView.as_view(), name='subcategories'),
        path('sidebar/', SidebarView.as_view(), name='sidebar'),
    ]))
]
