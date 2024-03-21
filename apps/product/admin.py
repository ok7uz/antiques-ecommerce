from django.contrib import admin
from django.forms import Textarea, TextInput
from django.db import models
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin

from apps.product.filters import CategoryFilter, CategoryDirectionFilter
from apps.product.inlines import ImagesInline, SubCategoryInline
from apps.product.models import Product, SubCategory, Category, ProductImage

admin.site.site_header = 'Администрация'
admin.site.site_title = 'Администрация'
admin.site.index_title = 'Добро пожаловать в администрацию АнтикДекор!'


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'is_new', 'price')
    fields = [
        ('is_new', 'image_preview'), 'name', 'vendor_code', 'category', 'price', 'description',
        'characteristic', 'size', 'history', 'video_url'
    ]
    search_fields = ['name', 'description', 'category__name', 'characteristic']
    list_filter = ['is_new', CategoryFilter]
    readonly_fields = ['image_preview']
    inlines = [ImagesInline]
    filter_horizontal = ('category',)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': '100%'})},
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
    }

    def image_preview(self, obj):
        image_model = obj.images.first()
        if image_model:
            url = image_model.image.url
            return mark_safe(f'<a href="{url}" target="_blank"><img src="{url}" height="150px"></a>')
        return 'Нет изображения'

    image_preview.short_description = ''

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'is_top', 'is_left']
    fields = ['name', 'is_top', 'is_left',]
    readonly_fields = []
    search_fields = ['name']
    list_filter = [CategoryDirectionFilter]
    inlines = [SubCategoryInline]


@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'parent']
    fields = ['name', 'parent']
    search_fields = ['name', 'parent__name', 'parent__parent__name']
    list_filter = [CategoryFilter]
    # inlines = [ProductInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = Category.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(ProductImage)
class ProductImageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['product', 'image']
    fields = ['product', 'image']
    search_fields = ['product__name', 'image']
