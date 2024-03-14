from django.contrib import admin
from django.forms import Textarea
from django.db import models
from django.utils.safestring import mark_safe

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
    list_display = ['name']
    readonly_fields = ['image_preview']
    fields = ['name', ('image', 'image_preview')]
    inlines = [CategoryInline]
    search_fields = ['name']

    def image_preview(self, obj):
        image = obj.image
        if image:
            image_url = image.url
            return mark_safe(f'<a href="{image_url}" target="_blank"><img src="{image_url}" height="80px"></a>')
        return 'No image'

    image_preview.short_description = 'preview'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ['name', 'parent']
    search_fields = ['name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = MainCategory.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
