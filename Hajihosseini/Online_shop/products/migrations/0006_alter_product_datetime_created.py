# Generated by Django 5.0.6 on 2024-07-18 13:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_datetime_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='datetime_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Time of Creation'),
        ),
    ]
