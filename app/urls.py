from django.urls import path
from .views import RegisterView, LoginView, PostView, FollowCreateView, UnfollowCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('create-post/', PostView.as_view(), name='create_post'),
    path('follow/', FollowCreateView.as_view(), name='follow'),
    path('unfollow/', UnfollowCreateView.as_view(), name='unfollow'),
]
