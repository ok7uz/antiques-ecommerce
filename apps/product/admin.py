from django import forms
from django.contrib import admin
from django.db.models import Q
from itertools import chain
from django.forms import Textarea, TextInput
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.product.filters import MainCategoryFilter, CategoryFilter
from apps.product.inlines import ImagesInline, ProductInline, CategoryInline, SubCategoryInline
from apps.product.models import Product, MainCategory, SubCategory, Category, BaseCategory, Genre

admin.site.site_header = 'Администрация'
admin.site.site_title = 'Администрация'
admin.site.index_title = 'Добро пожаловать в администрацию АнтикДекор!'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    fields = [
        'name', 'vendor_code', 'category', 'authorship', 'genre', 'price',
        'is_new', 'description', 'size', 'history', 'video_url'
    ]
    search_fields = ['name', 'description', 'category__name']
    list_filter = ['is_new', MainCategoryFilter]
    inlines = [ImagesInline]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': '100%'})},
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = BaseCategory.objects.filter(sub_categories__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['image_preview']
    fields = ['name', ('image', 'image_preview')]
    inlines = [CategoryInline]
    search_fields = ['name']

    def image_preview(self, obj):
        image = obj.image
        if image:
            image_url = image.url
            return mark_safe(f'<a href="{image_url}" target="_blank"><img src="{image_url}" height="100px"></a>')
        return ''

    image_preview.short_description = ''


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'parent', 'get_products']
    readonly_fields = ['get_products']
    search_fields = ['name']
    inlines = [SubCategoryInline]
    list_filter = [MainCategoryFilter]

    def get_products(self, obj):
        print(obj.sub_categories.all())
        if not obj.sub_categories.all():
            products = obj.products.all()
            if not products:
                return 'Нет продукта'

            return_html = ''
            for product in products:
                product_link = reverse('admin:product_product_change', args=[product.id])
                return_html += f'<a href="{product_link}">{product.name}</a><br>'
            return mark_safe(return_html)
        else:
            return 'Эта категория имеет подкатегории. В них расположены продукты'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = MainCategory.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    get_products.short_description = 'Продукты'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'parent', 'get_products']
    readonly_fields = ['get_products']
    search_fields = ['name', 'parent__name', 'parent__parent__name']
    list_filter = [MainCategoryFilter, CategoryFilter]

    def get_products(self, obj):
        products = obj.products.all()

        if not products:
            return 'Нет продукта'

        return_html = ''

        for product in products:
            product_link = reverse('admin:product_product_change', args=[product.id])
            return_html += f'<a href="{product_link}">{product.name}</a><br>'
        print(return_html)
        return mark_safe(return_html)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = Category.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    get_products.short_description = 'Продукты'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ['name']
    search_fields = ['name']
