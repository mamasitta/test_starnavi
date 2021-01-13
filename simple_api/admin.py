from django.contrib import admin
from .models import Post, Post_dislike, Post_like, User_activity

# Register your models here.
admin.site.register(Post)
admin.site.register(Post_like)
admin.site.register(Post_dislike)
admin.site.register(User_activity)
