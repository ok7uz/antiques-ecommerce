# Generated by Django 5.0.3 on 2024-03-16 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
        migrations.AddField(
            model_name='product',
            name='authorship',
            field=models.CharField(choices=[('western_europe', 'Западная Европа'), ('russian_period', 'Русский период'), ('soviet_period', 'Советский период')], default='western_europe', max_length=15, verbose_name='Авторство'),
            preserve_default=False,
        ),
    ]
