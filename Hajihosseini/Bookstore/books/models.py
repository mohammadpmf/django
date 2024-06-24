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
    book_creator = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='ایجاد کننده کتاب', related_name='books')

    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})
    

class Comment(models.Model):
    text = models.TextField(verbose_name='متن نظر')
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name='زمان آخرین تغییر')
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, verbose_name='کتاب', related_name='comments')
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='کاربر', related_name='comments')
    is_approved = models.BooleanField(default=False, verbose_name='تایید')
    is_recommended = models.BooleanField(default=True, verbose_name='پیشنهاد می شود')
    
    def __str__(self):
        return f"{self.user}: {self.text}"


class Favorite(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, verbose_name='کتاب', related_name='favorites')
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name='کاربر', related_name='favorites')
    
    class Meta:
        unique_together = ('book', 'user')