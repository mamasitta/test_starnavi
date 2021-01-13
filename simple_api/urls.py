from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/user_signup/', views.user_signup, name='register_user'),
    path('api/login/', views.login_view, name='login'),
    path('api/create_post/', views.create_post, name='create_post'),
    path('api/post_like/', views.post_like_save, name='post_like_save'),
    path('api/post_dislike/', views.post_dislike_save, name='post_dislike_save'),
    path('api/analytics/', views.analytics, name='analytics'),
    path('api/get_all_posts/', views.get_all_posts, name='get_all_posts'),
    path('api/user_activity/', views.user_activity, name='user_activity')
]