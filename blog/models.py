from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.

class Post(models.Model):
    # to manage the status of the blog post
    # i.e. either to save as draft or to publish
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'Pb', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
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

    class Meta:
        ordering = ['-publish']
        # also this?
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
