# Generated by Django 5.0.6 on 2024-07-14 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='status',
            new_name='active',
        ),
    ]
