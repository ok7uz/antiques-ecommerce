from django.db import models


class NewProductsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_new=True)


class MainCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent=None)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent__isnull=False, parent__parent=None)


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent__parent__isnull=False)
