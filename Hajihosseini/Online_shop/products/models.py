from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django_prose_editor.fields import ProseEditorField


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    # description = models.TextField(verbose_name=_('Description'))
    description = ProseEditorField(verbose_name=_('Description'))
    short_description = models.TextField(max_length=300, blank=True, verbose_name=_('Short description')) # حاجی حسینی این مکس لنگث رو برداشته بود و تو اچ تی ام ال فیلتر زده بود. اما من گذاشتم خودش تو تکست فیلد پنل ادمین اجازه تایپ بیشتر از ۳۰۰ کاراکتر رو نمیده. خیلی خفنه. اما فیلترش رو هم تو اچ تی ام ال گذاشتم که باشه.
    price = models.PositiveIntegerField(default=0, verbose_name=_('Price'))
    active = models.BooleanField(default=True, verbose_name=_('Active State'))
    image = models.ImageField(upload_to='product/product_cover', blank=True, verbose_name=_("Product Image"))
    datetime_created = models.DateTimeField(default=timezone.now, verbose_name=_("Date Time of Creation"))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_("Date Time of last edit"))

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Product"))
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', verbose_name=_("Author"))
    body = models.TextField(verbose_name=_('Comment Body'))
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS, verbose_name=_('Score to this product'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Time of Creation"))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_("Date Time of last edit"))
    active = models.BooleanField(default=True, verbose_name=_("Active State"))

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.product.pk})
    