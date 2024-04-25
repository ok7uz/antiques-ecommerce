from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin

from apps.main_page.models import Video, Banner, News, Expert
from config.utils import image_preview


@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['title', 'type']
    search_fields = ['title', 'url']
    readonly_fields = ['_image']
    list_filter = ['type']
    fields = ['title', 'type', 'url', ('banner', '_image')]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
        models.URLField: {'widget': TextInput(attrs={'size': '100%'})},
    }

    def _image(self, obj):
        image = obj.banner
        return image_preview(image, height=200, width=150)

    _image.short_description = ''


@admin.register(Banner)
class BannerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['title']
    readonly_fields = ['_image']
    search_fields = ['title', 'subtitle']
    fields = ['title', 'subtitle', ('image', '_image'), 'has_button', 'button_url']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
    }

    def _image(self, obj):
        image = obj.image
        return image_preview(image, height=180, width=300)

    _image.short_description = ''


@admin.register(News)
class NewsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['title', 'date']
    readonly_fields = ['_image']
    search_fields = ['title', 'content']
    list_filter = ['date']
    fields = ['title', ('image', '_image'), 'content']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
    }

    def _image(self, obj):
        image = obj.image
        return image_preview(image, height=150, width=200)

    _image.short_description = ''


@admin.register(Expert)
class ExpertAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'about']
    readonly_fields = ['_image']
    search_fields = ['name', 'about']
    fields = ['name', ('image', '_image'), 'about']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100%'})},
    }

    def _image(self, obj):
        image = obj.image
        return image_preview(image, height=150, width=200)

    _image.short_description = ''


admin.site.unregister(User)
admin.site.unregister(Group)
