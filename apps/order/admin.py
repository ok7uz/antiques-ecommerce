from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Order, OrderItem


class OrderProductInline(admin.TabularInline):
    model = OrderItem
    fields = ['product']
    readonly_fields = ['product']
    show_change_link = True
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['__str__', 'total_price', 'status', 'created']
    search_fields = ['id', 'customer_name', 'customer_phone']
    list_filter = ['status', 'created']
    ordering = ['-created']
    fields = ['customer_name', 'customer_phone', 'customer_email', 'customer_address', 'total_price', 'status']
    readonly_fields = ['customer_name', 'customer_phone', 'customer_email', 'customer_address', 'total_price']
    inlines = [OrderProductInline]

    def has_add_permission(self, request, obj=None):
        return False
