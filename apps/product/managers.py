from django.db import models


class MainCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent=None)


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent__isnull=False, parent__parent=None)
