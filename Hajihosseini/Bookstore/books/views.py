from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Book, Comment


class BookListView(generic.ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by=4


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self,*args, **kwargs):
        book=kwargs.get('object')
        context={
            'book': book,
            'comments': Comment.objects.filter(is_approved=True, book=book.pk).order_by('-datetime_modified')
            }
        return context


def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # comments = Comment.objects.filter(is_approved=True, book=book.pk).order_by('-datetime_modified')
    comments = book.comments.filter(is_approved=True, book=book.pk).order_by('-datetime_modified')
    context = {
        'book': book,
        'comments': comments,
    }
    return render(request, 'books/book_detail.html', context)


class BookCreateView(generic.CreateView):
    model = Book
    template_name = 'books/book_form.html'
    fields = ['title', 'author', 'description', 'price', 'cover', 'translator', 'publisher', 'year_published', 'number_of_pages', 'book_creator']


class BookUpdateView(generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover', 'translator', 'publisher', 'year_published', 'number_of_pages', 'book_creator']
    template_name = 'books/book_update_form.html'
    # context_object_name = 'book'


class BookDeleteView(generic.DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    context_object_name = 'book'
    success_url = reverse_lazy('books')
