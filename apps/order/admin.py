from django.contrib import admin
from django.utils.html import format_html

from .models import Order, OrderItem


class OrderProductInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'image_preview']
    readonly_fields = ['product', 'image_preview']
    show_change_link = True
    can_delete = False

    def image_preview(self, obj):
        images = obj.product.images.all()
        if images:
            url = obj.product.images.first().image.url
            return format_html(f'<a href="{url}" target="_blank"><img src="{url}" height="100px"></a>')
        return 'Нет изображения'

    image_preview.short_description = ''

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'total_price', 'status', 'created']
    search_fields = ['id', 'customer_name', 'customer_phone']
    list_filter = ['status', 'created']
    ordering = ['-created']
    fields = ['customer_name', 'customer_phone', 'customer_email', 'customer_address', 'total_price', 'status']
    readonly_fields = ['customer_name', 'customer_phone', 'customer_email', 'customer_address', 'total_price']
    inlines = [OrderProductInline]

    def has_add_permission(self, request, obj=None):
        return False
