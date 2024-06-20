from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('p', 'Published'),
        ('d', 'Draft'),
    )
    title = models.CharField(max_length=256, verbose_name='عنوان')
    text = models.TextField(verbose_name='متن پست')
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} written by {self.author.first_name} {self.author.last_name}"
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    

class Comment(models.Model):
    blogpost = models.ForeignKey(to=BlogPost, on_delete=models.CASCADE, related_name='comments', verbose_name='پست مربوطه در وبلاگ')
    commentor = models.CharField(max_length=256, blank=True, verbose_name='نام کامنت گذار')
    email = models.EmailField(blank=True, verbose_name='آدرس ایمیل کامنت گذار')
    text = models.TextField(verbose_name='متن کامنت')
    is_confirmed = models.BooleanField(default=False, verbose_name='وضعیت تایید کامنت')
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال کامنت')

    def __str__(self):
        if self.commentor.strip()!=0:
            return f"{self.commentor}: {self.text[:60]}"
        return f"Ananymous User: {self.text[:60]}"
