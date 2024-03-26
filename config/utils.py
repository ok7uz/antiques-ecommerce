from django.db.models import Q
from django.utils.html import format_html


def image_preview(image, height=100):
    if image:
        image_url = image.url
        return format_html(f'<a href="{image_url}" target="_blank"><img src="{image_url}" height="{height}px"></a>')
    return 'Нет изображения'


def get_by_category_id(request, queryset):
    category_id = request.query_params.get('category_id', None)
    if category_id:
        queryset = queryset.filter(category__id=category_id)
        return queryset
    return queryset


def get_by_sidebar_id(request, queryset):
    sidebar_id = request.query_params.get('sidebar_id', None)
    if sidebar_id:
        queryset = queryset.filter(category__id=sidebar_id)
        return queryset
    return queryset


def get_by_search(request, queryset):
    search = request.query_params.get('search', None)
    if search:
        search_conditions = Q()
        search_conditions |= Q(name__icontains=search)
        search_conditions |= Q(category__name__icontains=search)
        search_conditions |= Q(category__parent__name__icontains=search)
        search_conditions |= Q(description__icontains=search)
        search_conditions |= Q(vendor_code__icontains=search)
        search_conditions |= Q(history__icontains=search)
        search_conditions |= Q(characteristic__icontains=search)
        search_conditions |= Q(size__icontains=search)
        queryset = queryset.filter(search_conditions).distinct()
    queryset = queryset.prefetch_related('category', 'category__parent')
    return queryset
