from django.contrib import admin
from django.forms import Textarea, TextInput
from django.db import models
from import_export.admin import ImportExportModelAdmin

from apps.product.filters import CategoryFilter, CategoryDirectionFilter, ProductCategoryFilter, \
    ProductSubCategoryFilter
from apps.product.inlines import ImagesInline, SubCategoryInline
from apps.product.models import Product, SubCategory, Category
from config.utils import image_preview

admin.site.site_header = 'Администрация'
admin.site.site_title = 'Администрация'
admin.site.index_title = 'Добро пожаловать в администрацию АнтикДекор!'


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'vendor_code', 'is_new', 'price')
    fields = [
        ('is_new', '_image'), 'name', 'vendor_code', 'categories', 'price', 'description',
        'characteristic', 'size', 'history', 'video_url'
    ]
    search_fields = ['name', 'description', 'categories__name', 'characteristic', 'history']
    list_filter = ['is_new', ProductCategoryFilter, ProductSubCategoryFilter]
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


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'is_top', 'is_left']
    fields = ['name', 'is_top', 'is_left',]
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
