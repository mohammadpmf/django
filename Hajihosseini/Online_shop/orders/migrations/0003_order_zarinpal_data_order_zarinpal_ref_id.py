# Generated by Django 5.0.6 on 2024-07-20 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_zarinpal_authority_alter_order_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='zarinpal_data',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='zarinpal_ref_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
