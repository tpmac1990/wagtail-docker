from wagtail.models import Page

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()

class HomePage(Page):
    pass


# Post and Retry have been created to test elastic search. Go to the path below to test it
# app/home/management/commands/load_posts.py
class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=128, db_index=True, null=True)
    draft = models.BooleanField(default=True)

    user = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'home'


class Reply(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name='replies', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        app_label = 'home'
        verbose_name_plural = 'Replies'
