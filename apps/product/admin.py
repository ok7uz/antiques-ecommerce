from django.contrib import admin
from django.forms import Textarea
from django.db import models

from apps.product.inlines import ImagesInline, SubcategoryInline, ProductInline
from apps.product.models import Product, Category, Subcategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    readonly_fields = []
    search_fields = ('name', 'description')
    list_filter = ('subcategory', )
    inlines = [ImagesInline]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': '100%'})},
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [SubcategoryInline]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('category',)
    inlines = [ProductInline]
