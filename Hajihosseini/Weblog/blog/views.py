from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import BlogPost


def post_list_view(request):
    posts = BlogPost.objects.filter(status='p')
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
