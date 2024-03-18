import uuid
from django.db import models

from apps.product.managers import MainCategoryManager, SubCategoryManager, CategoryManager, NewProductsManager


class BaseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название', max_length=128)
    parent = models.ForeignKey('self', verbose_name='Высшая категория', on_delete=models.CASCADE,
                               related_name='sub_categories', null=True)
    image = models.ImageField('Изображение', upload_to='category/', null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        str_name = self.name
        parent = self.parent

        while parent:
            str_name = f'{parent.name} / ' + str_name
            parent = parent.parent

        return str_name


class MainCategory(BaseCategory):
    objects = MainCategoryManager()

    class Meta:
        proxy = True
        verbose_name = 'Главная категория'
        verbose_name_plural = 'Главная категории'


class Category(BaseCategory):
    objects = CategoryManager()

    class Meta:
        proxy = True
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(BaseCategory):
    objects = SubCategoryManager()

    class Meta:
        proxy = True
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Genre(models.Model):
    name = models.CharField('Название', max_length=128)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название продукта', max_length=255, unique=True, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField('Описание')

    price = models.PositiveIntegerField('Цена')
    is_new = models.BooleanField('Новый?', default=False)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    vendor_code = models.CharField('Артикул', max_length=32)
    history = models.CharField('История', max_length=255)
    characteristic = models.CharField('Характеристики', max_length=255)
    size = models.TextField('Размер')
    video_url = models.URLField('Ссылка на видео о продукте на YouTube', blank=True, null=True)

    AUTHORSHIP_CHOICES = {
        'western_europe': 'Западная Европа',
        'russian_period': 'Русский период',
        'soviet_period': 'Советский период',
    }
    authorship = models.CharField('Авторство', max_length=15, choices=AUTHORSHIP_CHOICES, blank=False, null=False)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='products', blank=True, null=True)

    objects = models.Manager()
    new_products = NewProductsManager()

    class Meta:
        ordering = ['-created', 'name']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='images')
    image = models.ImageField(upload_to='products/', null=True, blank=True, default=None)

    objects = models.Manager()

    class Meta:
        verbose_name = 'product image'
        verbose_name_plural = 'product images'

    def __str__(self):
        return self.image.url
