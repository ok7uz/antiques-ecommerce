from django.contrib import admin

from apps.product.models import Category, SubCategory


class CategoryFilter(admin.SimpleListFilter):
    title = 'Категории'
    parameter_name = 'category_id'

    def lookups(self, request, model_admin):
        print(model_admin)
        queryset = Category.objects.all()
        return queryset.values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if self.value() is not None:
            try:
                queryset = queryset.filter(parent__id=category_id)
                return queryset
            except queryset.model.DoesNotExist:
                return None

        return queryset


class ProductCategoryFilter(admin.SimpleListFilter):
    title = 'Категории'
    parameter_name = 'category_id'

    def lookups(self, request, model_admin):
        print(model_admin)
        queryset = Category.objects.filter(is_top=True)
        return queryset.values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if self.value() is not None:
            try:
                queryset = queryset.filter(category__id=category_id)
                return queryset
            except queryset.model.DoesNotExist:
                return None

        return queryset


class ProductSubCategoryFilter(admin.SimpleListFilter):
    title = 'Подкатегории'
    parameter_name = 'subcategory_id'

    def lookups(self, request, model_admin):
        print(model_admin)
        queryset = SubCategory.objects.all()
        return queryset.values_list('id', 'name')

    def queryset(self, request, queryset):
        subcategory_id = self.value()
        if self.value() is not None:
            try:
                queryset = queryset.filter(category__id=subcategory_id)
                return queryset
            except queryset.model.DoesNotExist:
                return None

        return queryset


class CategoryDirectionFilter(admin.SimpleListFilter):
    title = 'Категория направления'
    parameter_name = 'direction'

    def lookups(self, request, model_admin):
        return [('top', 'Верхнее меню'), ('left', 'Левое меню')]

    def queryset(self, request, queryset):
        direction = self.value()
        if direction == 'top':
            try:
                queryset = queryset.filter(is_top=True)
                return queryset
            except queryset.model.DoesNotExist:
                return None
        elif direction == 'left':
            try:
                queryset = queryset.filter(is_left=True)
                return queryset
            except queryset.model.DoesNotExist:
                return None

        return queryset
