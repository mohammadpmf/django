from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import BlogPost
from django.contrib.auth import get_user_model


def post_list_view(request):
    posts = BlogPost.objects.filter(status='p').order_by('-datetime_created')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/posts_list.html', context=context)


def post_detail_view(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context=context)

def post_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        BlogPost.objects.create(
            title = title,
            text = text,
            author = get_user_model().objects.last(),
            status = 'p',
        )
        return redirect('posts_list')
    else:
        print('get')
    return render(request, 'blog/post_create.html')