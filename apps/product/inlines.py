from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.product.models import Product, ProductImage, Subcategory


class ImagesInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}" height="50px"></a>')
        return 'No image'

    image_preview.short_description = 'image'


class ProductInline(admin.TabularInline):
    model = Product
    fields = ('link_to_product', 'price', 'image_preview')
    readonly_fields = ('link_to_product', 'price', 'image_preview')
    can_delete = False
    extra = 0

    def link_to_product(self, obj):
        link = reverse('admin:product_product_change', args=[obj.id])
        return mark_safe('<a href="{}">{}</a>'.format(link, obj.name))

    def image_preview(self, obj):
        product_image = obj.images.first()
        if product_image:
            image_url = product_image.image.url
            return mark_safe(f'<a href="{image_url}" target="_blank"><img src="{image_url}" height="50px"></a>')
        return 'No image'

    image_preview.short_description = 'image'
    link_to_product.short_description = 'name'


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
