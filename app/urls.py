from django.urls import path
from .views import RegisterView, LoginView, PostView, FollowCreateView, LikeView, DislikeView, CommentView, \
    UnfollowView, ListOwnFollower, ListOwnFollowing

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('create-post/', PostView.as_view(), name='create_post'),
    path('like/', LikeView.as_view(), name='like_post'),
    path('dislike/', DislikeView.as_view(), name='dislike_post'),
    path('comment/', CommentView.as_view(), name='comment_post'),
    path('follow/', FollowCreateView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UnfollowView.as_view(), name='unfollow'),
    path('followers/', ListOwnFollower.as_view(), name='followers'),
    path('followings/', ListOwnFollowing.as_view(), name='followings'),
]
