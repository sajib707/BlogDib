from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from .models import Category, Blogs, Comment, Author
from .forms import CommentForm
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import BlogSearchForm
from django.db.models import Count



def categories(request):
    return {
        'categories': Category.objects.all()
    }


def index(request):
    blogs = Blogs.objects.filter(is_published=True)
    eblogs = Blogs.objects.filter(is_editors_pick=True)
    tblogs = Blogs.objects.filter(is_trending_post=True)
    pblogs = Blogs.objects.filter(is_popular_blog=True)
    authors = Author.objects.all()
    categories = Category.objects.annotate(blog_count=Count('category'))
    paginator = Paginator(blogs, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'blogs': blogs, 
                                          'eblogs': eblogs, 
                                          'tblogs': tblogs, 
                                          'pblogs': pblogs, 
                                          'authors': authors, 
                                          'page_obj': page_obj,
                                          'categories': categories})


def all_blogs(request, slug=None):
    all_blogs = Blogs.objects.all().order_by("-date_created")
    authors = Author.objects.all()
    categories = Category.objects.annotate(blog_count=Count('category'))
    paginator = Paginator(all_blogs, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'all_blogs.html', {'all_blogs' : all_blogs, 
                                             'authors': authors,
                                             'categories':categories, 
                                             "page_obj": page_obj})

def all_authors(request, slug=None):
    authors = Author.objects.all()
    return render(request,'all_authors.html', {'all_authors' : authors})

def author_detail(request, slug):
    author_detail = get_object_or_404(Author, slug=slug)
    filter_blogs = Blogs.objects.filter(author=author_detail.user, is_published=True)
    num_blogs = filter_blogs.count()
    return render(request,'author_details.html', {'author_detail' : author_detail, 'filter_blogs': filter_blogs, 'num_blogs':num_blogs})

def filter_blogs(request, slug=None): 
    category = get_object_or_404(Category, slug=slug)
    filter_blogs = Blogs.objects.filter(category = category)
    paginator = Paginator(filter_blogs, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'filter_blogs.html', {'category' : category, 
                                                'filter_blogs' : filter_blogs,
                                                'page_obj': page_obj})


def blog_detail(request, slug):
    blog_detail = get_object_or_404(Blogs, slug=slug)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                name=form.cleaned_data["name"],
                comment=form.cleaned_data["comment"],
                blog=blog_detail,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(blog=blog_detail)
    context = {
        "blog_detail": blog_detail,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request,'blog_details.html', context)


def blog_search(request):
    form = BlogSearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = BlogSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            if not query.strip():  
                return redirect('myBlog:index')
            results = Blogs.objects.filter(
                Q(title__icontains=query) | 
                Q(body__icontains=query) | 
                Q(tags__name__icontains=query),
                is_published=True  
            ).distinct()

    return render(request, 'blog_search.html', {'form': form, 'query': query, 'results': results})

def about(request):
    return render(request,'about_us.html')

def contact(request):
    return render(request,'contact.html')