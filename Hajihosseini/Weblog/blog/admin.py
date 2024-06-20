from django.contrib import admin
from .models import BlogPost, Comment


# مدل دوم با استفاده از دکوریتور
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'author', 'likes', 'datetime_modified']
    list_display_links = ['title', 'author', 'likes', 'datetime_modified']
    list_editable = ['status']
    ordering = ['-status', '-likes', 'id']


# مدل اول 
# admin.site.register(BlogPost, BlogPostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'blogpost', 'commentor', 'email', 'is_confirmed']
    list_display_links = ['id', 'blogpost', 'commentor', 'email']
    list_editable = ['is_confirmed']
