from django.contrib import admin

from .models import Category, Blogs, Author, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'approved')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'slug', 'author', 'image', 'image_credit',
                    'body', 'date_published', 'is_published')
    list_filter = ('is_published', 'date_created', 'date_published', 'author',)
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'date_published'
    ordering = ['is_published', '-date_created', ]
    readonly_fields = ('views', 'count_words', 'read_time')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comment', 'blog', 'date_created', )
    list_filter = ('date_created', 'name',)
    search_fields = ('name', 'blog', 'comment')
    date_hierarchy = 'date_created'
    ordering = ['-date_created', ]
    readonly_fields = ('name', 'email', 'comment', 'blog', 'date_created', 'date_updated',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('image', 'bio', 'job_title', 'facebook_url', 'twitter_url', 'linkedin_url', 'github_url')

