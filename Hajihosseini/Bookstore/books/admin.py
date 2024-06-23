from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'year_published', 'book_creator']
    list_display_links = ['title', 'author', 'price', 'year_published', 'book_creator']
