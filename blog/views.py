from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404


def post_list(request):
    posts = Post.published.all()
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def post_detail(request, pk):
    # try:
    #     post = Post.published.get(id=pk)
    # except Post.DoesNotExist:
    #     raise Http404("NO POST FOUND")
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )