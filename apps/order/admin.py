from django.contrib import admin

from utils import image_preview
from .models import Order, OrderItem


class OrderProductInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', '_image']
    readonly_fields = ['product', '_image']
    show_change_link = True
    can_delete = False

    def _image(self, obj):
        image = obj.banner
        return image_preview(image, 100)

    _image.short_description = ''

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
