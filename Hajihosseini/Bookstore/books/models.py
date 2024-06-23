from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان کتاب')
    author = models.CharField(max_length=255, default='جک لندن', verbose_name='نویسنده')
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=9.99, verbose_name='قیمت')
    cover = models.ImageField(upload_to='covers/', blank=True, verbose_name='عکس جلد')
    translator = models.CharField(max_length=255, blank=True, verbose_name='مترجم')
    publisher = models.CharField(max_length=255, blank=True, verbose_name='ناشر')
    year_published = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='سال انتشار')
    number_of_pages = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='تعداد صفحات کتاب')
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد کتاب')
    book_creator = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='ایجاد کننده کتاب')

    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})
    