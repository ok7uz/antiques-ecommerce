from django.db import models

from apps.product.models import Product


class Order(models.Model):
    customer_name = models.CharField('Имя клиента', max_length=255)
    customer_phone = models.CharField('Телефон клиента', max_length=20)
    customer_email = models.EmailField('Email клиента')
    customer_address = models.TextField('Адрес клиента')

    created = models.DateTimeField('Дата создания', auto_now_add=True)
    status = models.CharField('Статус', max_length=32, choices=[
        ('pending', 'В ожидании'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Отменено'),
    ], default='pending')

    items = models.ManyToManyField(Product, through='OrderItem', related_name='orders')
    total_price = models.PositiveIntegerField('Сумма заказа')

    class Meta:
        ordering = ['-created']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.id} - {self.customer_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказы', on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, verbose_name='Продукты', on_delete=models.CASCADE, related_name='orderitems')
    
    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
        
    def __str__(self):
        return f"{self.product.name} для Заказа #{self.order.id}"


class Callback(models.Model):
    applicant_name = models.CharField('Имя заявителя', max_length=255)
    applicant_email = models.EmailField('Электронная почта заявителя')
    created = models.DateField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связи'

    def __str__(self):
        return self.applicant_name
