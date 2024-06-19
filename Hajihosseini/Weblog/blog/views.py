from django.shortcuts import render, redirect, reverse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import BlogPost
from .forms import BlogPostForm


def post_list_view(request):
    posts = BlogPost.objects.filter(status='p').order_by('-datetime_modified')
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
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect('post_detail', form.pk)
    else:
        form = BlogPostForm()
    context = {'form': form}
    return render(request, 'blog/post_create.html', context)


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
