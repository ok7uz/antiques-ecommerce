from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_sold=False)


class NewProductsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_new=True)


class SoldProductsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_sold=True)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent=None)


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent__isnull=False, parent__parent=None)


class L3CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent__parent__isnull=False)
