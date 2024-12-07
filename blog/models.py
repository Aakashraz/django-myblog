from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )


class Post(models.Model):
    # to manage the status of the blog post
    # i.e. either to save as draft or to publish
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'Pb', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        # to prevent the Post model from storing duplicated posts by defining slug to be unique.
        unique_for_date='publish'
    )
    # This field defines a many-to-one relationship with the default user model,
    # meaning that each post is written by a user, and a user can write any number of posts.
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # need to understand the below code
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager

    class Meta:
        ordering = ['-publish']
        # also this?
        indexes = [
            models.Index(fields=['-publish']),
        ]

    # initializing tags
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ]
                       )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']
        indexes = [models.Index(fields=['created_on'])]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
