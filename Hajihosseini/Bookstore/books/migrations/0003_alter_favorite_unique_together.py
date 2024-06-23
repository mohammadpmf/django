# Generated by Django 5.0.4 on 2024-06-23 18:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_book_creator_comment_favorite'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('book', 'user')},
        ),
    ]
