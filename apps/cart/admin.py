from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.cart.models import CartItem, Cart


class CardItemsInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ('product', 'image', 'quantity')
    extra = 0

    def image(self, obj):
        image_url = obj.product.product_images.first().image.url
        return mark_safe(f'<img src="{image_url}" height="80px">')

    image.short_description = 'image'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'created']
    readonly_fields = []
    list_filter = ['created']
    inlines = [CardItemsInline]
