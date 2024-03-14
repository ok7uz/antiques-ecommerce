from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['date', 'title']
    readonly_fields = ['image_preview']
    search_fields = ['title', 'content']
    list_filter = ['date']
    fields = ['title', 'subtitle', ('image', 'image_preview'), 'content']

    def image_preview(self, obj):
        image = obj.image
        if image:
            image_url = image.url
            return mark_safe(f'<a href="{image_url}" target="_blank"><img src="{image_url}" height="80px"></a>')
        return 'No image'

    image_preview.short_description = 'preview'
