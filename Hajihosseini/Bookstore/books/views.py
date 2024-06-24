from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Book, Comment
from .forms import CommentForm


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
        comment_form = CommentForm()
        context={
            'book': book,
            'comments': Comment.objects.filter(is_approved=True, book=book.pk).order_by('-datetime_modified'),
            'comment_form': comment_form,
            }
        return context
    
    def post(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        text = request.POST.get('text')
        is_recommended = request.POST.get('is_recommended')
        if is_recommended == 'on':
            is_recommended = True
        else:
            is_recommended = False
        # توضیح این که وقتی تیک رو میزدیم، مقدار رو میفرستاد و داخلش مینوشت on که یعنی
        # تیکش زده است و روشنه. اما وقتی تیکش رو برمیداشتیم کلا چیزی به اون اسم نمیفرستاد
        # و مقدارش None بود که مشکل ایجاد میکرد. خلاصه در هر دو حالت ارور میداد و نمیتونست
        # تو دیتابیس ذخیره کنه. خودم با ایف و الس بالا گفتم اگر آن بود مقدارش رو بذاره ترو
        # اگر هم on نبود که یعنی هیچی نفرستاده و None هست. اما نمیتونیم برای ساخت یک کامنت
        # مقدار این متغیر رو نان بذاریم. عوضش کردم به False
        book = get_object_or_404(Book, pk=pk)
        error = ""
        message = None
        if text!="":
            Comment.objects.create(text=text, is_recommended=is_recommended, book=book, user=request.user)
            message = f"نظر {text} از طرف {request.user} برای کتاب {book} با موفقیت ارسال شد. پس از تایید مدیریت در سایت نمایش داده خواهد شد.از نظر ارزشمند شما سپاسگزاریم."
        else:
            error = "متن نمیتواند خالی باشد."
        context={
            'book': book,
            'comments': Comment.objects.filter(is_approved=True, book=book).order_by('-datetime_modified'),
            'error': error,
            'comment_form': CommentForm(),
            'message': message,
            }
        return render(request, 'books/book_detail.html', context=context)


def book_detail_view(request, pk):
    message = None
    book = get_object_or_404(Book, pk=pk)
    # comments = Comment.objects.filter(is_approved=True, book=book.pk).order_by('-datetime_modified')
    comments = book.comments.filter(is_approved=True, book=book.pk).order_by('-datetime_modified')
    if request.method=='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.book = book
            comment_form.user = request.user
            comment_form.save()
            comment_form = CommentForm()
            message = f"نظر {request.POST.get('text')} از طرف {request.user} برای کتاب {book} با موفقیت ارسال شد. پس از تایید مدیریت در سایت نمایش داده خواهد شد.از نظر ارزشمند شما سپاسگزاریم."
    else:
        comment_form = CommentForm()
    context = {
        'book': book,
        'comments': comments,
        'comment_form': comment_form,
        'message': message,
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
