from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm


# for handling forms
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        # If the form is valid, the validated data is retrieved with form.cleaned_data. This attribute is a
        # dictionary of form fields and their values.
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
    else:
        form = EmailPostForm()

    return render(request,'blog/post/share.html', {
        'post': post,
        'form': form
    }
    )


# Class Based View for post_list
class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    # In ListView, following is the information related to pagination
    # paginator: The Paginator object
    # page_obj: The current page of objects
    # is_paginated: Boolean indicating if pagination is active

    def get_context_data(self, **kwargs):
        # First get the default context from the parent class (ListView)
        context = super().get_context_data(**kwargs)
        print("Context before pagination:", context)
        # Get the paginator object from the context
        paginator = context['paginator']
        # Retrieve the page number from the GET request
        page_number = self.request.GET.get('page', 1)

        # Handle different pagination scenarios
        try:
            page_number = int(page_number)
            posts = paginator.page(page_number)

        except (ValueError, PageNotAnInteger):
            # Default to first page if page is not an integer
            posts = paginator.page(1)
        except EmptyPage:
            # Default to last page if page is out of range
            posts = paginator.page(paginator.num_pages)

        # Update the paginated posts to the context
        context['posts'] = posts
        print("Final context:", context)
        return context


# Function Based View for post_list
def post_list(request):
    published_list = Post.published.all()
    paginator = Paginator(published_list, 3)
    page_number = request.GET.get('page', 1)
    # We retrieve the page GET HTTP parameter and store it in the page_number variable.
    # This parameter contains the requested page number. If the page parameter is not in the GET parameters
    # of the request, we use the default value 1 to load the first page of results.
    try:
        posts = paginator.page(page_number)
    # We obtain the objects for the desired page by calling the page() method of Paginator. This
    # method returns a Page object that we store in the posts variable.
    except (EmptyPage, PageNotAnInteger) as e:
        # if page_number is not an integer get the first page
        if isinstance(e, PageNotAnInteger):
            posts = paginator.page(1)

        # if page_number is out of range get last page or results
        else:
            # paginator.num_pages will return total no. os pages, which is also last page no.
            posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.published.get(id=pk)
    # except Post.DoesNotExist:
    #     raise Http404("NO POST FOUND")

    # to check the value fetched from the URL pattern.
    print(f"Year: {year}")
    print(f"Month: {month}")
    print(f"Day: {day}")
    print(f"Post slug: {post}")

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )


# example use of reverse and redirect
def redirect_me(request):
    url = reverse('blog:post_detail', kwargs={'pk': 10})
    return redirect(url)