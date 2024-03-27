# Generated by Django 5.0.3 on 2024-03-27 09:22

import ckeditor_uploader.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('subtitle', models.CharField(max_length=255, verbose_name='Подзаголовок')),
                ('image', models.ImageField(upload_to='banner/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Контент')),
                ('image', models.ImageField(upload_to='news/', verbose_name='Изображение')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('url', models.URLField(verbose_name='Ссылка на YouTube')),
                ('banner', models.ImageField(upload_to='video-banner/', verbose_name='Изображение для видео')),
            ],
            options={
                'verbose_name': 'видео',
                'verbose_name_plural': 'видео',
                'ordering': ['-id'],
            },
        ),
    ]
