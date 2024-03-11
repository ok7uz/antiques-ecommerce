from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.product.models import Product, ProductImage, Category


class ProductImagesInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        print(obj.image)
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" height="80px">')
        return 'No image'

    image_preview.short_description = 'IMAGE'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    readonly_fields = []
    inlines = [ProductImagesInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
