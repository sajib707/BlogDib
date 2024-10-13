from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from .blog_utils import count_words, read_time
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField()
    approved = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('myBlog:filter_blogs',
                       kwargs={'slug': self.slug})
    


class Blogs(models.Model):

    # Article status constants
    DRAFTED = "DRAFTED"
    PUBLISHED = "PUBLISHED"

    # CHOICES
    STATUS_CHOICES = (
        (DRAFTED, 'Draft'),
        (PUBLISHED, 'Publish'),
    )


    # BLOG MODEL FIELDS
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='category')
    title = models.CharField(max_length=250, null=False, blank=False)
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blogs')
    image = models.ImageField(default='blog-default.jpg',
                              upload_to='blog_pics')
    image_credit = models.CharField(max_length=250, null=True, blank=True)
    body = RichTextUploadingField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    date_published = models.DateTimeField(null=True, blank=True,
                                          default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    count_words = models.CharField(max_length=50, default=0)
    read_time = models.CharField(max_length=50, default=0)
    is_editors_pick = models.BooleanField(default=False)
    is_trending_post = models.BooleanField(default=False)
    is_popular_blog = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


    class Meta:
        unique_together = ("title",)
        ordering = ('-date_published',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        self.count_words = count_words(self.body)
        self.read_time = read_time(self.body)
        super(Blogs, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('myBlog:blog_detail', kwargs={'slug': self.slug})
    

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, help_text="Enter you full name")
    slug = models.SlugField(max_length=255)
    image = models.ImageField(default='profile-pic-default.jpg',
                              upload_to='profile_pics')
    
    job_title = models.CharField(max_length=100)
    bio = models.CharField(max_length=100,
                           help_text="Short Bio (eg. I love cats and games)")

    twitter_url = models.CharField(max_length=250, default="#",
                                   blank=True, null=True,
                                   help_text=
                                   "Enter # if you don't have an account")
    linkedin_url = models.CharField(max_length=250, default="#",
                                     blank=True, null=True,
                                     help_text=
                                     "Enter # if you don't have an account")
    facebook_url = models.CharField(max_length=250, default="#",
                                    blank=True, null=True,
                                    help_text=
                                    "Enter # if you don't have an account")
    github_url = models.CharField(max_length=250, default="#",
                                  blank=True, null=True,
                                  help_text=
                                  "Enter # if you don't have an account")

    created_on = models.DateTimeField(default=timezone.now)

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_absolute_url(self):
        return reverse('myBlog:author_detail', kwargs={'slug': self.slug})
    

class Comment(models.Model):

    name = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField()
    comment = models.TextField(null=False, blank=False)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Comment by {self.name} on {self.blog}"