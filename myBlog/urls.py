from django.urls import path

from . import views

app_name = 'myBlog'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('all_blogs', views.all_blogs, name='all_blogs'),
    path('blog-<slug:slug>', views.filter_blogs, name='filter_blogs'),
    path('details-<slug:slug>', views.blog_detail, name='blog_detail'),
    path('all_authors', views.all_authors, name='all_authors'),
    path('author-details-<slug:slug>', views.author_detail, name='author_detail'),
    path('search/', views.blog_search, name='blog_search'),
    path('about/', views.about, name='about'),   
    path('contact/', views.contact, name='contact'),  
]