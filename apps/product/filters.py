from django.contrib import admin

from apps.product.models import Category, SubCategory


class CategoryFilter(admin.SimpleListFilter):
    title = 'Категории'
    parameter_name = 'category_id'

    def lookups(self, request, model_admin):
        queryset = Category.objects.filter(subcategories__isnull=False).distinct()
        return queryset.values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id is not None:
            queryset = queryset.filter(parent__id=category_id)
        return queryset


class ProductCategoryFilter(admin.SimpleListFilter):
    title = 'Категории'
    parameter_name = 'category_id'

    def lookups(self, request, model_admin):
        queryset = Category.objects.filter(is_top=True)
        return queryset.values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id is not None:
            queryset = queryset.filter(categories__id=category_id)
        return queryset


class SidebarFilter(admin.SimpleListFilter):
    title = 'Категории левого меню'
    parameter_name = 'sidebar_id'

    def lookups(self, request, model_admin):
        category_id = request.GET.get('category_id', None)
        queryset = SubCategory.objects.filter(parent__is_left=True)
        if category_id:
            queryset = queryset.filter(products__categories=category_id).distinct()
        return queryset.values_list('id', 'name')

    def queryset(self, request, queryset):
        sidebar_id = self.value()
        if sidebar_id is not None:
            queryset = queryset.filter(categories__id=sidebar_id)
        return queryset


class CategoryDirectionFilter(admin.SimpleListFilter):
    title = 'Категория направления'
    parameter_name = 'direction'

    def lookups(self, request, model_admin):
        return [('top', 'Верхнее меню'), ('left', 'Левое меню')]

    def queryset(self, request, queryset):
        direction = self.value()
        if direction == 'top':
            queryset = queryset.filter(is_top=True)
        elif direction == 'left':
            queryset = queryset.filter(is_left=True)
        return queryset
