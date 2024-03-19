from django.contrib import admin
from django.forms import Textarea, TextInput, CheckboxSelectMultiple
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.product.filters import CategoryFilter, CategoryDirectionFilter
from apps.product.inlines import ImagesInline, CategoryInline, SubCategoryInline
from apps.product.models import Product, SubCategory, Category, BaseCategory

admin.site.site_header = 'Администрация'
admin.site.site_title = 'Администрация'
admin.site.index_title = 'Добро пожаловать в администрацию АнтикДекор!'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    fields = [
        'name', 'vendor_code', 'category', 'price',
        'is_new', 'description', 'size', 'history', 'video_url'
    ]
    search_fields = ['name', 'description', 'category__name']
    list_filter = ['is_new', CategoryFilter]
    inlines = [ImagesInline]
    filter_horizontal = ('category',)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': '100%'})},
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
        # models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = BaseCategory.objects.filter(sub_categories__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'top_menu', 'left_menu',]
    readonly_fields = []
    search_fields = ['name']
    list_filter = [CategoryDirectionFilter]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'parent', 'get_products']
    readonly_fields = ['get_products']
    search_fields = ['name', 'parent__name', 'parent__parent__name']
    list_filter = [CategoryFilter]

    def get_products(self, obj):
        products = obj.products.all()

        if not products:
            return 'Нет продукта'

        return_html = ''

        for product in products:
            product_link = reverse('admin:product_product_change', args=[product.id])
            return_html += f'<a href="{product_link}">{product.name}</a><br>'
        print(return_html)
        return mark_safe(return_html)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = Category.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    get_products.short_description = 'Продукты'
