from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group

from apps.main_page.models import Video, Banner, News


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'url']
    fields = ['name', 'url']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title']
    readonly_fields = ['image_preview']
    search_fields = ['title', 'subtitle']
    fields = ['title', 'subtitle', ('image', 'image_preview')]

    def image_preview(self, obj):
        image = obj.image
        if image:
            image_url = image.url
            return mark_safe(f'<a href="{image_url}" target="_blank"><img src="{image_url}" height="200px"></a>')
        return 'Нет изображения'

    image_preview.short_description = ''


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['date', 'title']
    readonly_fields = ['image_preview']
    search_fields = ['title', 'content']
    list_filter = ['date']
    fields = ['title', ('image', 'image_preview'), 'content']

    def image_preview(self, obj):
        image = obj.image
        if image:
            image_url = image.url
            return mark_safe(f'<a href="{image_url}" target="_blank"><img src="{image_url}" height="100px"></a>')
        return 'Нет изображения'

    image_preview.short_description = ''


admin.site.unregister(User)
admin.site.unregister(Group)
