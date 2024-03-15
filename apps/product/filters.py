from django.contrib import admin
from django.db.models import Q

from apps.product.models import MainCategory, Category, SubCategory, Product


class MainCategoryFilter(admin.SimpleListFilter):
    title = 'Главная категории'
    parameter_name = 'main_category_id'

    def lookups(self, request, model_admin):
        queryset = MainCategory.objects.all()
        return queryset.values_list('id', 'name')

    def queryset(self, request, queryset):
        model = queryset.model
        main_category_id = self.value()
        if self.value() is not None:
            try:
                if model == Category:
                    queryset = queryset.filter(parent__id=main_category_id)
                elif model == SubCategory:
                    queryset = queryset.filter(parent__parent__id=main_category_id)
                elif model == Product:
                    queryset = queryset.filter(
                        Q(category__parent__parent__id=main_category_id) | Q(category__parent__parent__id=main_category_id)
                    )
                else:
                    return None
                return queryset
            except queryset.model.DoesNotExist:
                return None

        return queryset


class CategoryFilter(admin.SimpleListFilter):
    title = 'Категории'
    parameter_name = 'category_id'

    def lookups(self, request, model_admin):
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
