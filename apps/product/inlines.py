from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.product.models import ProductImage, SubCategory


class ImagesInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['image_preview']
    verbose_name = 'Изображение продукта'
    verbose_name_plural = 'Изображения продуктов'
    show_change_link = True
    extra = 1

    def image_preview(self, obj):
        if obj.image:
            url = obj.image.url
            return mark_safe(f'<a href="{url}" target="_blank"><img src="{url}" height="100px"></a>')
        return 'Нет изображения'

    image_preview.short_description = ''


class SubCategoryInline(admin.TabularInline):
    verbose_name = 'Подкатегория'
    verbose_name_plural = 'Подкатегории'
    model = SubCategory
    fields = ['name']
    extra = 1
    show_change_link = True
