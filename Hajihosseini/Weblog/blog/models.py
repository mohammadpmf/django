from django.db import models
from django.contrib.auth import get_user_model

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