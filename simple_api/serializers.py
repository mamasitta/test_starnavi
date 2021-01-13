from django.contrib.auth.models import User
from rest_framework import serializers

from simple_api.models import Post, Post_like, Post_dislike, User_activity


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'last_login', 'date_joined']


class PostDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_dislike
        fields = ['post', 'date']


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post_like
        fields = ['post', 'date']


class PostSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    post_like = PostLikeSerializer(many=True)
    post_dislike = PostDislikeSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'post', 'date_created', 'post_like', 'post_dislike']


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = User_activity
        fields = ['date']


class UserActivitySerializer(serializers.HyperlinkedModelSerializer):
    last_activity = ActivitySerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'last_login', 'last_activity']



