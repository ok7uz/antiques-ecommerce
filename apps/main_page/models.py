import uuid

from django_ckeditor_5.fields import CKEditor5Field
from django.db import models


class Banner(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    subtitle = models.CharField('Подзаголовок', max_length=255)
    image = models.ImageField('Изображение', upload_to='banner/')
    has_button = models.BooleanField('Есть кнопка?', default=False)
    button_url = models.URLField('Ссылка на кнопку', null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.title


class Video(models.Model):
    title = models.CharField('Название', max_length=255)
    url = models.URLField('Ссылка на YouTube')
    banner = models.ImageField('Изображение для видео', upload_to='video-banner/')
    type = models.CharField(max_length=10, choices=(('main', 'основные'), ('event', 'мероприятие')))

    class Meta:
        ordering = ['-id']
        verbose_name = 'видео'
        verbose_name_plural = 'видео'

    def __str__(self):
        return self.title


class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField('Название', max_length=255)
    content = CKEditor5Field('Контент', config_name='extends')
    image = models.ImageField('Изображение', upload_to='news/')
    date = models.DateField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title


class Expert(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя и фамилия эксперта')
    about = models.TextField(verbose_name='Об эксперте')
    image = models.ImageField(upload_to='experts/', verbose_name='Фотография эксперта')

    class Meta:
        verbose_name = 'Эксперт'
        verbose_name_plural = 'Эксперты'

    def __str__(self):
        return self.name

