import datetime

import jwt
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import requests
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from simple_api.helpers.helpers import get_user_id_from_jwt
from simple_api.serializers import PostSerializer, PostLikeSerializer, PostDislikeSerializer, UserActivitySerializer
from .models import Post_dislike, Post_like, Post, User_activity

from test_starnavi import settings




@api_view(['POST'])
def user_signup(request):
    # getting data from post request
    data = request.data
    if 'email' in data:
        email = data['email']
    else:
        content = {'error': 'no email'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if 'username' in data and data['username'] is not None and len(data['username']) > 0:
        username = data['username']
    else:
        content = {'error': "No username"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if 'password' in data and data['password'] is not None and len(data['password']) > 0:
        password = data['password']
    else:
        content = {'error': "No password"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    # if username is not used save data in db
    is_username_used = User.objects.filter(username=username)
    if not is_username_used:
        hashed_password = make_password(password)
        new_user = User(email=email, password=hashed_password, username=username)
        new_user.save()
        user = User.objects.get(username=username)
        date = datetime.datetime.now()
        user_activity = User_activity(user_id=user.id, date=date)
        user_activity.save()
        # login user

        auth.login(request, user)
        # get JWT tokens for registered user and send them by API
        data = {"username": username, "password": password}
        response = requests.post('http://127.0.0.1:8000/api/token/', data=data)
        return Response(response.json(), status=status.HTTP_201_CREATED)
    else:
        content = {'error': 'This username is used'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(["post"])
def login_view(request):
    # getting data
    data = request.data
    if 'username' in data and data['username'] is not None and len(data['username']) > 0:
        username = data['username']
    else:
        content = {'error': "No username"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if 'password' in data and data['password'] is not None and len(data['password']) > 0:
        password = data['password']
    else:
        content = {'error': "No password"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    # if user exist creating jwt token
    is_user_exist = User.objects.get(username=username)
    # login user
    auth.login(request, is_user_exist)
    if is_user_exist:
        user_activity = User_activity.objects.filter(user_id=is_user_exist.id).update(date=datetime.datetime.now())
        data = {"username": username, "password": password}
        response = requests.post('http://127.0.0.1:8000/api/token/', data=data)
        return Response(response.json(), status=status.HTTP_200_OK)
    else:
        content = {'error': "user is not valid"}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_post(request):
    if "Authorization" in request.headers:
        # getting user_id from jwt token
        user_id = get_user_id_from_jwt(request.headers['Authorization'])
        data = request.data
        # checking all data from request
        if 'title' in data and data['title'] is not None and len(data['title']) > 0:
            title = data['title']
        else:
            content = {'error': "No title"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if 'post' in data and data['post'] is not None and len(data['post']) > 0:
            post = data['post']
        else:
            content = {'error': "No post"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        # add data to db and return details
        new_post = Post(user_id=user_id, title=title, post=post, date_created=datetime.datetime.now())
        new_post.save()
        user_activity = User_activity.objects.filter(user_id=user_id).update(date=timezone.now())
        post_created = Post.objects.filter(user_id=user_id, title=title, post=post)
        serializer = PostSerializer(post_created, many=True)
        return Response(serializer.data)
    else:
        content = {"error": "no jwt"}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def post_like_save(request):
    if "Authorization" in request.headers:
        # getting user_id from jwt token
        user_id = get_user_id_from_jwt(request.headers['Authorization'])
        data = request.data
        # checking data from request
        if 'post_id' in data and data['post_id'] is not None:
            post_id = data['post_id']
        else:
            content = {'error': "No post_id"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        # saving like to db and returning post with likes and dislikes
        new_like = Post_like(post_id=post_id, user_id=user_id, date=datetime.datetime.now())
        new_like.save()
        user_activity = User_activity.objects.filter(user_id=user_id).update(date=timezone.now())
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    else:
        content = {"error": "no jwt"}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def post_dislike_save(request):
    if "Authorization" in request.headers:
        # getting user_id from jwt token
        user_id = get_user_id_from_jwt(request.headers['Authorization'])
        data = request.data
        # checking data from request
        if 'post_id' in data and data['post_id'] is not None:
            post_id = data['post_id']
        else:
            content = {'error': "No post_id"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        # saving dislike and returning post with likes and dislikes
        new_dislike = Post_dislike(post_id=post_id, user_id=user_id, date=datetime.datetime.now())
        new_dislike.save()
        user_activity = User_activity.objects.filter(user_id=user_id).update(date=timezone.now())
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    else:
        content = {"error": "no jwt"}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)




@api_view(['GET'])
def analytics(request):
    if "Authorization" in request.headers:
        # getting user_id from jwt token
        user_id = get_user_id_from_jwt(request.headers['Authorization'])
        user_activity = User_activity.objects.filter(user_id=user_id).update(date=timezone.now())
        # getting data from request
        try:
            date_from = request.GET['date_from']
            date_to = request.GET["date_to"]
        except(TypeError, ValueError, OverflowError):
            content = {'error': 'No date from or date to'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        # getting all satisfied by data likes and dislikes from table
        likes = Post_like.objects.filter(date__range=[date_from, date_to])
        print(likes)
        dislikes = Post_dislike.objects.filter(date__range=[date_from, date_to])
        return Response({
            'likes': PostLikeSerializer(likes, many=True, context={'request': request}).data,
            'dislikes': PostDislikeSerializer(dislikes, many=True, context={"request": request}).data,
        })
    else:
        content = {"error": "no jwt"}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_all_posts(request):
    if "Authorization" in request.headers:
        # getting user_id from jwt token
        user_id = get_user_id_from_jwt(request.headers['Authorization'])
        user_activity = User_activity.objects.filter(user_id=user_id).update(date=timezone.now())
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    else:
        content = {"error": "no jwt"}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def user_activity(request):
    if "Authorization" in request.headers:
        # getting user_id from jwt token
        user_id = get_user_id_from_jwt(request.headers['Authorization'])
        user_activity = User_activity.objects.filter(user_id=user_id).update(date=timezone.now())
        # request with username
        if "username" in request.GET:
            user = User.objects.filter(username=request.GET['username'])
            if not user:
                content = {'error': "user is not valid"}
                return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                serializer = UserActivitySerializer(user)
                return Response(serializer.data)
        # request with user_id
        elif "user_id" in request.GET:
            user = User.objects.get(id=request.GET["user_id"])
            if not user:
                content = {'error': "user is not valid"}
                return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                serializer = UserActivitySerializer(user)
                return Response(serializer.data)
        # request for all registered users
        else:
            users = User.objects.all()
            serializer = UserActivitySerializer(users, many=True)
            return Response(serializer.data)
    else:
        content = {"error": "no jwt"}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)
