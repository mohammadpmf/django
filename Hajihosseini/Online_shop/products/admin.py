from django.contrib import admin

from .models import Product, Comment


class CommentsInline(admin.TabularInline):
    model = Comment
    fields = ['author', 'body', 'stars', 'active', ]
    extra=1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['title', 'description', 'price', 'active']
    list_display_links = ['title', 'description', 'price']
    list_editable = ['active']
    inlines = [CommentsInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['product', 'author', 'body', 'stars', 'active']
    list_display_links = ['product', 'author', 'body', 'stars']
    list_editable = ['active']