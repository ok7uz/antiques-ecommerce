import uuid

from django.db import models


def upload_to(instance, filename):
    print(instance)
    return 'images/{instance}/{filename}'.format(instance=instance.product.id, filename=filename)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

    objects = models.Manager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True, null=False, blank=False)
    category = models.ManyToManyField(Category, related_name='products')
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
    images = models.ManyToOneRel(to='ProductImage', field='image', field_name='images', related_name='product', on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='product_images')
    image = models.ImageField(upload_to=upload_to, null=True, blank=True, default=None)

    objects = models.Manager()

    def __str__(self):
        return self.product.name
