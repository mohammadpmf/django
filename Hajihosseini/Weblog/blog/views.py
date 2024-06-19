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
    form_class = BlogPostForm
    template_name = 'blog/post_create.html'
    # اگه گت ابسلوت یو آر ال تعریف کرده باشیم، ساکسس یو آر لازم نیست میره همونجا.
    # اما اگه نوشته باشیم و دلمون نخواد بره اونجا میتونیم از ساکسس یو آر ال استفاده کنیم.
    # اولویت با ساکسس یو آر ال هست.
    # اما از بین این دو تا حتما باید یکیش باشه. (حداقل) هر دو باشن میره به ساکسس یو آر ال
    # success_url = reverse_lazy('posts_list')
    
    # اگه نخوایم از فرم کلس استفاده کنیم این طوری هم میشه نوشت
    # model = BlogPost
    # fields = ['title', 'text', 'author', 'status']
    
class PostUpdateView(generic.UpdateView):
    model = BlogPost
    # اینجا مدل اجباری هست و باید بنویسیم. تو کریت ویو میتونستیم مدل رو ننویسیم و چون میخواست
    # فرم کلس رو بخوونه، تو کلاس متا نوشته بودیم که مدلش بلاگ پست هست و اونجا مشکلی نداشت.
    # چون همون لحظه میساخت. اما اینجا فرق داره. اینجا ما میخوایم اول بریم جزییات یک پست
    # رو بگیریم و اطلاعاتش رو میخواد از دیتابیس بپرسه. پس قبل از این که ما تغییرش بدیم میخواد
    # یک سری اطلاعات از چیزی به ما نشون بده. از چه چیزی؟؟ آهاااا. اینجاست که لازمه ما بهش بگیم
    # که مدل چی هست. چون اول میره از دیتابیس میگیرتش که اطلاعات رو به ما نشون بده. وقتی که ما
    # تغییرش میخوایم بدیم اونجا تازه میره سراغ فرم کلس که خب دیگه بهش گفتیم مدلش چی بوده.
    # به هر حال. چون آپدیت ترکیب سلکت و اینزرت هست، پس به همه اطلاعات اونها نیاز داره.
    form_class = BlogPostForm
    template_name = 'blog/post_create.html'


class PostDeleteView(generic.DeleteView):
    model = BlogPost
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('posts_list')
