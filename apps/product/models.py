import uuid
from django.db import models

from apps.product.managers import MainCategoryManager, SubCategoryManager


def upload_to(instance, filename):
    return 'products/{filename}'.format(instance=instance.product.id, filename=filename)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    image = models.ImageField(upload_to='category/', null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class MainCategory(Category):
    objects = MainCategoryManager()

    class Meta:
        proxy = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class SubCategory(Category):
    objects = SubCategoryManager()

    class Meta:
        proxy = True
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True, null=False, blank=False)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    art = models.CharField(max_length=150)
    history = models.CharField(max_length=150)
    characteristic = models.CharField(max_length=150)
    size = models.TextField()
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created', 'name']
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='images')
    image = models.ImageField(upload_to=upload_to, null=True, blank=True, default=None)

    objects = models.Manager()

    class Meta:
        verbose_name = 'product image'
        verbose_name_plural = 'product images'

    def __str__(self):
        return self.image.url
