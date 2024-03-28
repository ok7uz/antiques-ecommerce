# Generated by Django 5.0.3 on 2024-03-28 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Callback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_name', models.CharField(max_length=255, verbose_name='Имя заявителя')),
                ('applicant_email', models.EmailField(max_length=254, verbose_name='Электронная почта заявителя')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Обратная связь',
                'verbose_name_plural': 'Обратная связи',
                'ordering': ['-created'],
            },
        ),
    ]
