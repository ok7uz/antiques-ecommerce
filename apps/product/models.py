import uuid
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from apps.product.managers import SubCategoryManager, CategoryManager, NewProductsManager, SoldProductsManager, \
    ProductManager, L3CategoryManager


class BaseCategory(models.Model):
    name = models.CharField('Название', max_length=128, db_index=True)
    title = models.CharField('Заголовок', max_length=256, null=True, blank=True)
    description = models.TextField('Описание', null=True, blank=True)
    parent = models.ForeignKey('self', verbose_name='Высшая категория', on_delete=models.CASCADE,
                               related_name='subcategories', null=True, db_index=True, blank=True)
    image = models.ImageField('Изображение', upload_to='category/', null=True, blank=True)
    is_top = models.BooleanField('Верхнее меню?', default=False, db_index=True)
    is_left = models.BooleanField('Левое меню?', default=False, db_index=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-is_top', 'parent__id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        str_name = self.name
        parent = self.parent

        while parent:
            str_name = f'{parent.name} / ' + str_name
            parent = parent.parent

        return str_name


class Category(BaseCategory):
    objects = CategoryManager()

    class Meta:
        proxy = True
        ordering = ['-is_top', 'id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(BaseCategory):
    objects = SubCategoryManager()

    class Meta:
        proxy = True
        ordering = ['-parent__is_top', 'parent__name', 'name']
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class L3Category(BaseCategory):
    objects = L3CategoryManager()

    class Meta:
        proxy = True
        ordering = ['-parent__is_top', 'parent__name', 'name']
        verbose_name = 'Подподкатегория'
        verbose_name_plural = 'Подподкатегории'


class Product(models.Model):
    name = models.CharField('Название продукта', max_length=255, db_index=True)
    categories = models.ManyToManyField(
        BaseCategory, verbose_name='Категории', related_name='products',
        db_table='product_product_category'
    )
    description = CKEditor5Field('Описание', config_name='extends',)
    price = models.PositiveIntegerField('Цена')

    is_new = models.BooleanField('Новый?', default=False, db_index=True)
    is_sold = models.BooleanField('Продано?', default=False, db_index=True)

    created = models.DateField('Дата создания', auto_now_add=True)
    vendor_code = models.CharField('Артикул', max_length=32, db_index=True)
    history = models.CharField('История', max_length=255, db_index=True)
    characteristic = models.CharField('Характеристики', max_length=255, db_index=True)
    size = models.CharField('Размер', max_length=255, db_index=True)
    video_url = models.URLField('Ссылка на видео о продукте на YouTube', blank=True, null=True)

    commentary = models.TextField('Комментарий', blank=True, null=True)

    objects = ProductManager()
    new_products = NewProductsManager()

    class Meta:
        ordering = ['vendor_code', '-is_new', 'name']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class SoldProduct(Product):
    objects = SoldProductsManager()

    class Meta:
        proxy = True
        ordering = ['-is_new', 'name']
        verbose_name = 'Проданный продукт'
        verbose_name_plural = 'Проданная продукция'


def upload_to(instance, filename):
    return "product/{}-{}.jpg".format(instance.product.id, instance.product.images.count() + 1)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to, default=None)

    objects = models.Manager()

    class Meta:
        ordering = ['id']
        verbose_name = 'product image'
        verbose_name_plural = 'product images'

    def __str__(self):
        return self.image.url


class Filter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, verbose_name='Название')
    products = models.ManyToManyField(Product, related_name='filter', verbose_name='Продукты')

    class Meta:
        db_table = 'product_filter'
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'

    def __str__(self):
        return f"Фильтр '{self.name}'"
