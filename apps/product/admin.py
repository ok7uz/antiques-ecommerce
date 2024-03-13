from django.contrib import admin
from django.forms import Textarea
from django.db import models

from apps.product.inlines import ImagesInline, ProductInline, CategoryInline
from apps.product.models import Product, MainCategory, SubCategory


admin.site.site_header = 'AntikDecor Administration'
admin.site.site_title = 'AntikDecor Admin'
admin.site.index_title = 'Welcome to AntikDecor Administration!'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    readonly_fields = []
    search_fields = ['name', 'description', 'category__name']
    autocomplete_fields = ['category']
    list_filter = ('category', )
    inlines = (ImagesInline, )

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': '100%'})},
    }


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    fields = ['name']
    inlines = [CategoryInline]
    search_fields = ['name']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
