from django.contrib import admin

from .models import Book, Comment, Favorite


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'year_published', 'book_creator']
    list_display_links = ['title', 'author', 'price', 'year_published', 'book_creator']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'book', 'user', 'is_recommended', 'is_approved']
    list_display_links = ['text', 'book', 'user', 'is_recommended']
    list_editable = ['is_approved']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['book', 'user']
    list_display_links = ['book', 'user']
