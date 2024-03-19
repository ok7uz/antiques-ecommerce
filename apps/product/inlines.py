from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.product.models import Product, ProductImage, Category, SubCategory


class ImagesInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['image_preview']
    verbose_name = 'Изображение продукта'
    verbose_name_plural = 'Изображения продуктов'
    show_change_link = True

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}" height="50px"></a>')
        return 'Нет изображения'

    image_preview.short_description = 'Изображение'


class ProductInline(admin.TabularInline):
    model = Product
    # fields = ('name', 'price', 'image_preview')
    # readonly_fields = ('name', 'price', 'image_preview')
    can_delete = False
    extra = 0
    show_change_link = True

    def image_preview(self, obj):
        product_image = obj.images.first()
        if product_image:
            image_url = product_image.image.url
            return mark_safe(f'<a href="{image_url}" target="_blank"><img src="{image_url}" height="50px"></a>')
        return 'No image'

    image_preview.short_description = 'image'


class SubCategoryInline(admin.TabularInline):
    verbose_name = 'Подкатегория'
    verbose_name_plural = 'Подкатегории'
    model = SubCategory
    # readonly_fields = ['name']
    fields = ['name']
    extra = 1
    show_change_link = True
