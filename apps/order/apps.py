from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.order'
    verbose_name = 'Заказ и обратная связь'
    verbose_name_plural = 'Заказы и обратная связи'
