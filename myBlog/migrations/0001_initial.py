# Generated by Django 5.1 on 2024-10-04 21:07

import django.db.models.deletion
import django.utils.timezone
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='profile-pic-default.jpg', upload_to='profile_pics')),
                ('job_title', models.CharField(max_length=100)),
                ('bio', models.CharField(help_text='Short Bio (eg. I love cats and games)', max_length=100)),
                ('twitter_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=250, null=True)),
                ('linkedin_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=250, null=True)),
                ('facebook_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=250, null=True)),
                ('github_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=250, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('approved', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField()),
                ('image', models.ImageField(default='blog-default.jpg', upload_to='blog_pics')),
                ('image_credit', models.CharField(blank=True, max_length=250, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('date_published', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('views', models.PositiveIntegerField(default=0)),
                ('count_words', models.CharField(default=0, max_length=50)),
                ('read_time', models.CharField(default=0, max_length=50)),
                ('is_editors_pick', models.BooleanField(default=False)),
                ('is_trending_post', models.BooleanField(default=False)),
                ('is_popular_blog', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='myBlog.category')),
            ],
            options={
                'ordering': ('-date_published',),
                'unique_together': {('title',)},
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.TextField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('approved', models.BooleanField(default=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myBlog.blogs')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
    ]
