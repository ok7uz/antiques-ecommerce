from django.contrib import admin
from django.forms import Textarea, TextInput
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from apps.order.models import Order
from apps.product.filters import CategoryFilter, CategoryDirectionFilter, ProductCategoryFilter, \
    SidebarFilter
from apps.product.inlines import ImagesInline, SubCategoryInline
from apps.product.models import Product, SubCategory, Category, SoldProduct
from config.utils import image_preview

admin.site.site_header = 'Администрация'
admin.site.site_title = 'Администрация'
admin.site.index_title = 'Добро пожаловать в администрацию АнтикДекор!'


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'vendor_code', 'is_new', 'price')
    fields = [
        ('is_new', '_image'), 'name', 'vendor_code', 'categories', 'price', 'description',
        'characteristic', 'size', 'history', 'video_url', 'is_sold'
    ]
    search_fields = ['name', 'description', 'categories__name', 'characteristic', 'history']
    list_filter = ['is_new', ProductCategoryFilter, SidebarFilter]
    readonly_fields = ['_image']
    inlines = [ImagesInline]
    filter_horizontal = ['categories']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': '100%'})},
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
        models.URLField: {'widget': TextInput(attrs={'size': '100%'})},
    }

    def _image(self, obj):
        image = obj.images.first().image
        return image_preview(image, 150)

    _image.short_description = ''


@admin.register(SoldProduct)
class SoldProductAdmin(ProductAdmin):
    list_display = ('name', 'vendor_code', 'price')
    fields = [
        ('is_new', '_image'), 'name', 'vendor_code', 'categories', 'price', 'description',
        'characteristic', 'size', 'history', 'video_url', 'is_sold', '_order'
    ]
    readonly_fields = ['_image', '_order']

    def _order(self, obj):
        order = Order.objects.filter(items=obj).first()
        if order:
            print(Order._meta.app_label)
            url = reverse("admin:%s_%s_change" % (Order._meta.app_label, Order._meta.model_name), args=[order.id])
            return format_html(f'<a href="{url}">{order.__str__()}</a>')
        return 'Не найдено'

    _order.short_description = 'Заказ'

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'is_top', 'is_left']
    fields = ['name', 'is_top', 'is_left']
    search_fields = ['name']
    list_filter = [CategoryDirectionFilter]
    inlines = [SubCategoryInline]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
    }


@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'parent']
    fields = ['name', 'parent']
    search_fields = ['name', 'parent__name']
    list_filter = [CategoryFilter]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = Category.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
