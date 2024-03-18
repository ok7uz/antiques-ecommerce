from django.contrib import admin

from apps.product.models import Product
from .models import Order, OrderItem


class OrderProductInline(admin.TabularInline):
    model = OrderItem
    fields = ['product']
    readonly_fields = ['product']
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['id', 'customer_name', 'customer_phone']
    list_filter = ['status', 'created']
    ordering = ['-created']
    # readonly_fields = ['total_price']
    inlines = [OrderProductInline]

    # def has_add_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return obj and obj.status != 'delivered'


admin.site.register(OrderItem)
