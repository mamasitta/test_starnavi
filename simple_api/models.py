from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=255)
    post = models.TextField()
    date_created = models.DateTimeField()


class Post_like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')


class Post_dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_dislike')
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_dislike')


class User_activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='last_activity')
    date = models.DateTimeField()