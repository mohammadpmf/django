from django.shortcuts import render, redirect, reverse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views import generic
from django.urls import reverse_lazy

from .models import BlogPost
from .forms import BlogPostForm


class PostListView(generic.ListView):
    # model = BlogPost # اگه کوئری ست بنویسیم دیگه مدل تو خودش معلوم هست. ننویسیم هم اشکال نداره. بنویسیم هم که بهتره. فقط کامنت کردم که تست کنم.
    queryset = BlogPost.objects.filter(status='p').order_by('-datetime_modified')
    template_name = 'blog/posts_list.html'
    # اگه متغیر تمپلیت نیم رو نذاریم، خود جنگو اسم مدل رو حروف کوچیک میکنه تهش یه آندرلاین میذاره و کلمه
    # لیست رو بهش میچسبونه. یعنی اگه مشخص نکنم که تمپلیت نیم چی هست، جنگو اینجا دنبال این میگرده
    # blog/blogpost_list.html
    context_object_name = 'posts'
    # اگه متغیر کانتکست آبجکت نیم رو نذاریم، خود جنگو اسم مدل رو حروف کوچیک میکنه. تهش یه آندرلاین میذاره
    # و بعد هم کلمه لیست رو میذاره. یعنی اینجا میشه
    # blogpost_list


class PostDetailView(generic.DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    # اگه متغیر تمپلیت نیم رو نذاریم، خود جنگو اسم مدل رو حروف کوچیک میکنه تهش یه آندرلاین میذاره و کلمه
    # دیتیل رو بهش میچسبونه. یعنی اگه مشخص نکنم که تمپلیت نیم چی هست، جنگو اینجا دنبال این میگرده
    # blog/blogpost_detail.html
    context_object_name = 'post'
    # اگه متغیر کانتکست آبجکت نیم رو نذاریم، خود جنگو اسم مدل رو حروف کوچیک میکنه. یعنی اینجا میشه
    # blogpost

class PostCreateView(generic.CreateView):
    # form_class = BlogPostForm
    template_name = 'blog/post_create.html'
    # اگه گت ابسلوت یو آر ال تعریف کرده باشیم، ساکسس یو آر لازم نیست میره همونجا.
    # اما اگه نوشته باشیم و دلمون نخواد بره اونجا میتونیم از ساکسس یو آر ال استفاده کنیم.
    # اولویت با ساکسس یو آر ال هست.
    # اما از بین این دو تا حتما باید یکیش باشه. (حداقل) هر دو باشن میره به ساکسس یو آر ال
    # success_url = reverse_lazy('posts_list')
    
    # اگه نخوایم از فرم کلس استفاده کنیم این طوری هم میشه نوشت
    # model = BlogPost
    # fields = ['title', 'text', 'author', 'status']
    
# def post_create_view(request):
#     if request.method == 'POST':
#         form = BlogPostForm(request.POST)
#         if form.is_valid():
#             form = form.save()
#             return redirect('post_detail', form.pk)
#     else:
#         form = BlogPostForm()
#     context = {'form': form}
#     return render(request, , context)


def post_update_view(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    form = BlogPostForm(request.POST or None, instance=post)
    if form.is_valid():
        form = form.save()
        return redirect('post_detail', form.pk)
    # if request.method == 'POST':
    #     form = BlogPostForm(request.POST, instance=post)
    #     if form.is_valid():
    #         form = form.save()
    #         return redirect('post_detail', form.pk)
    # else:
    #     form = BlogPostForm(instance=post)
    return render(request, 'blog/post_create.html', context={'form': form})


def post_delete_view(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method=='POST':
        post.delete()
        return redirect('posts_list')
    return render(request, 'blog/post_delete.html', context={'post': post})
