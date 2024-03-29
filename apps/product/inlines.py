from django.contrib import admin
from django.db import models
from django.forms import TextInput

from apps.product.models import ProductImage, SubCategory
from config.utils import image_preview


class ImagesInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['_image']
    verbose_name = 'Изображение продукта'
    verbose_name_plural = 'Изображения продуктов'
    extra = 1

    def _image(self, obj):
        image = obj.image
        return image_preview(image, height=100, width=100)

    _image.short_description = ''


class SubCategoryInline(admin.TabularInline):
    verbose_name = 'Подкатегория'
    verbose_name_plural = 'Подкатегории'
    model = SubCategory
    fields = ['name']
    extra = 1
    show_change_link = True
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
    }
