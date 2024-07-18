from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django_prose_editor.fields import ProseEditorField


class Product(models.Model):
    title = models.CharField(max_length=100)
    # description = models.TextField()
    description = ProseEditorField()
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    image = models.ImageField(verbose_name=_("Product Image"), upload_to='product/product_cover', blank=True)
    datetime_created = models.DateTimeField(verbose_name=_("Date Time of Creation"), default=timezone.now)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    PRODUCT_STARS = (
        ('1', _('Very Bad')),
        ('2', _('Bad')),
        ('3', _('Normal')),
        ('4', _('Good')),
        ('5', _('Perfect')),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name=_('Comment Body'))
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS, verbose_name=_('Score to this product'))
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.product.pk})
    
