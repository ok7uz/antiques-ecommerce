from django.urls import path

from apps.product.views import ProductView, ProductListView, CategoryView, CategoryListView, SubcategoryView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('<uuid:id>/', ProductView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<uuid:id>/', CategoryView.as_view(), name='category-detail'),
    path('subcategory/<uuid:id>/', SubcategoryView.as_view(), name='category-detail')
]
