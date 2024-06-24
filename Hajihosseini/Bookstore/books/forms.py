from django import forms

from .models import Book, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'is_recommended', )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'description', 'price', 'cover', 'translator', 'publisher', 'year_published', 'number_of_pages', )
