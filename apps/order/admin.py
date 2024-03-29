from django.contrib import admin

from config.utils import image_preview
from .models import Order, OrderItem, Callback


class OrderProductInline(admin.TabularInline):
    model = OrderItem
    fields = ['_image', 'product', '_price']
    readonly_fields = ['product', '_image', '_price']
    show_change_link = True
    can_delete = False

    def _image(self, obj):
        image = obj.product.images.first().image
        return image_preview(image, height=120, width=120)

    def _price(self, obj):
        return obj.product.price

    _image.short_description = ''
    _price.short_description = 'Цена'

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


@admin.register(Callback)
class CallbackAdmin(admin.ModelAdmin):
    list_display = ['applicant_name', 'applicant_email', 'created']
    readonly_fields = ['applicant_name', 'applicant_email']
    search_fields = ['applicant_name', 'applicant_email']
    list_filter = ['created']
    fields = ['applicant_name', 'applicant_email']

    def has_add_permission(self, request, obj=None):
        return False
