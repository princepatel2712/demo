from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('create_post/', PostCreateView.as_view(), name='create-post'),
    path('update_post/<int:pk>/', PostUpdateView.as_view(), name='update-post'),
    path('like/', LikeView.as_view(), name='like-post'),
    path('dislike/', DislikeView.as_view(), name='dislike-post'),
    path('comment/', CommentView.as_view(), name='comment-post'),
    path('follow/', FollowCreateView.as_view(), name='follow'),
    path('unfollow/', UnfollowView.as_view(), name='unfollow'),
    path('followers/', ListOwnFollower.as_view(), name='followers'),
    path('followings/', ListOwnFollowing.as_view(), name='followings'),
]
