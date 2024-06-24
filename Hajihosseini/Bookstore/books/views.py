from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .models import Book, Comment
from .forms import BookForm, CommentForm


class BookListView(generic.ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by=4


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self,*args, **kwargs): # اگه بخوایم تابع get_context_data رو بنویسیم، kwargs رو نمیشه حذف کرد. خودش کلید آبجکت رو به صورت kwargs میفرسته.
        # book=kwargs.get('object') # اول ازش این شکلی استفاده کرده بودم. بعد تابع get_object رو یاد گرفتم که به نظرم خیلی قشنگ تر و تمیز تره
        book = self.get_object()
        context={
            'book': book,
            'comments': Comment.objects.filter(is_approved=True, book=book.pk).order_by('-datetime_modified'),
            'comment_form': CommentForm(),
            }
        return context
    
    # @login_required # این رو وقتی میذاشتم، موقعی که لاگین نبود بهم گیر میداد.
    # اما خودم بدون این توی اچ تی ام ال بررسی کردم که اگه لاگین نیست اصلا فرم رو نشون نده.
    # با این حال اگه بشه به یه روشی فه این یو آر ال پست کرد و اطلاعات رو فرستاد، باز احتمالا
    # ارور بده. اما روشی که خودش ساخته بود جالب نبود. کلا اگه لاگین نبودی نمیتونستی اطلاعات
    # کتاب رو هم ببینی. مال من میشه دید. اما نمیشه کامنت گذاشت و باید لاگین کرد. حالا اگه
    # کسی یه جوری یه متد پست بفرسته که بدون لاگین بخواد کامنت بذاره، بهش ارور میده.
    def post(self, request, *args, **kwargs):
        book = self.get_object()
        comments = Comment.objects.filter(is_approved=True, book=book).order_by('-datetime_modified')
        comment_form = CommentForm(request.POST)
        message = None
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.book = book
            comment_form.user = request.user
            comment_form.save()
            message = f"نظر {request.POST.get('text')} از طرف {request.user} برای کتاب {book} با موفقیت ارسال شد. پس از تایید مدیریت در سایت نمایش داده خواهد شد.از نظر ارزشمند شما سپاسگزاریم."
            comment_form = CommentForm()
        context={
            'book': book,
            'comments': comments,
            'comment_form': comment_form,
            'message': message,
            }
        return render(request, 'books/book_detail.html', context)


def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # comments = Comment.objects.filter(is_approved=True, book=book.pk).order_by('-datetime_modified')
    comments = book.comments.filter(is_approved=True, book=book.pk).order_by('-datetime_modified')
    comment_form = CommentForm()
    message = None
    if request.method=='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.book = book
            comment_form.user = request.user
            comment_form.save()
            message = f"نظر {request.POST.get('text')} از طرف {request.user} برای کتاب {book} با موفقیت ارسال شد. پس از تایید مدیریت در سایت نمایش داده خواهد شد.از نظر ارزشمند شما سپاسگزاریم."
            comment_form = CommentForm()
    context = {
        'book': book,
        'comments': comments,
        'comment_form': comment_form,
        'message': message,
        }
    return render(request, 'books/book_detail.html', context)


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    
    def post(self, request):
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            book_form = book_form.save(commit=False)
            book_form.user = self.request.user
            book_form.save()
            return redirect(book_form.get_absolute_url())
        context = {'form': book_form}
        return render(request, 'books/book_form.html', context)


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_update_form.html'
    context_object_name = 'book'

    def test_func(self):
        object = self.get_object()
        return object.user==self.request.user
    
    def post(self, request, *args, **kwargs): # اینجا حتما باید kwargs باشه. خودش پرایمری کی رو میاد میفرسته. وقتی نمیذاشتم ارور میداد که ارسال شده اما این تابع پست انتظارش رو نداشته. پس میذاریم که انتظارش رو داشته باشه :)
        book:Book = self.get_object()
        book_form = BookForm(request.POST, request.FILES, instance=book)
        if book_form.is_valid():
            book_form = book_form.save()
            return redirect(book.get_absolute_url())
        # اول این رو این مدلی که پایین نوشتم نوشته بودم که کار هم میکرد.
        # اما داشتم تست میکردم دیدم که ایف مدل بالایی
        # هم جواب میده. از نظر منطقی درسته. چون بهش گفتم این بوک فورمه، اینستنسش همون بوک هست.
        # پس قاعدتا اطلاعات رو داره و هر چیزی رو که رکوئست دات پست براش ارسال کرده جایگزین میکنه
        # اما چون یوزر رو ارسال نکرده، خودش همون یوزر قبلی رو میذاره. به هر حال کد پایینی جامع تر
        # و طولانی تر هست. اما پاکش نکردم و کامنت کردم و گذاشتم بمونه که یادم نره و اگه تو حالت
        # خاص مشکلی پیش اومد، سه ساعت وقتم گرفته نشه و کد آماده شو داشته باشم.
        # if book_form.is_valid():
        #     book_form = book_form.save(commit=False)
        #     book_form.user = book.user
        #     book_form.save()
        #     return redirect(book.get_absolute_url())
        context = {'form': book_form, 'book': book}
        return render(request, 'books/book_update_form.html', context)



class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    context_object_name = 'book'
    success_url = reverse_lazy('books')

    def test_func(self):
        object = self.get_object()
        return object.user==self.request.user
