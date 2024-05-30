from django.shortcuts import render
from .models import BlogPost


def post_list_view(request):
    posts = BlogPost.objects.filter(status='p')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/posts_list.html', context=context)

