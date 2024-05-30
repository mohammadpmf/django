from django.contrib import admin
from .models import BlogPost


# مدل دوم با استفاده از دکوریتور
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'author', 'likes', 'datetime_modified']
    list_display_links = ['author', 'likes', 'datetime_modified']
    list_editable = ['status']
    ordering = ['-status', '-likes', 'id']


# مدل اول 
# admin.site.register(BlogPost, BlogPostAdmin)