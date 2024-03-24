from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from apps.main_page.models import Video, Banner, News


@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title', 'url']
    readonly_fields = ['image_preview']
    fields = ['title', 'url', ('banner', 'image_preview')]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
        models.URLField: {'widget': TextInput(attrs={'size': '100%'})},
    }

    def image_preview(self, obj):
        image = obj.banner
        if image:
            image_url = image.url
            return format_html(f'<a href="{image_url}" target="_blank"><img src="{image_url}" height="100px"></a>')
        return 'Нет изображения'

    image_preview.short_description = ''


@admin.register(Banner)
class BannerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['title']
    readonly_fields = ['image_preview']
    search_fields = ['title', 'subtitle']
    fields = ['title', 'subtitle', ('image', 'image_preview')]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
    }

    def image_preview(self, obj):
        image = obj.image
        if image:
            image_url = image.url
            return format_html(f'<a href="{image_url}" target="_blank"><img src="{image_url}" height="200px"></a>')
        return 'Нет изображения'

    image_preview.short_description = ''


@admin.register(News)
class NewsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['title', 'date']
    readonly_fields = ['image_preview']
    search_fields = ['title', 'content']
    list_filter = ['date']
    fields = ['title', ('image', 'image_preview'), 'content']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
    }

    def image_preview(self, obj):
        image = obj.image
        if image:
            image_url = image.url
            return format_html(f'<a href="{image_url}" target="_blank"><img src="{image_url}" height="100px"></a>')
        return 'Нет изображения'

    image_preview.short_description = ''


admin.site.unregister(User)
admin.site.unregister(Group)
