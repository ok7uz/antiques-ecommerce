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
    fields = ('name', 'price', 'image_preview')
    readonly_fields = ('name', 'price', 'image_preview')
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


class CategoryInline(admin.TabularInline):
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'
    model = Category
    fields = ['name', 'link_to_category']
    readonly_fields = ['link_to_category']
    extra = 1

    def link_to_category(self, obj):
        print(obj)
        if not obj.name:
            return ''
        link = reverse('admin:product_category_change', args=[obj.id])
        return mark_safe(f'<a href="{link}">Посмотреть</a>')

    link_to_category.short_description = ''


class SubCategoryInline(admin.TabularInline):
    verbose_name = 'Подкатегория'
    verbose_name_plural = 'Подкатегории'
    model = SubCategory
    readonly_fields = ['link_to_sub_category']
    fields = ['name', 'link_to_sub_category']
    extra = 1

    def link_to_sub_category(self, obj):
        if not obj.name:
            return ''
        link = reverse('admin:product_subcategory_change', args=[obj.id])
        return mark_safe(f'<a href="{link}">Посмотреть</a>')

    link_to_sub_category.short_description = ''
