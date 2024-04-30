from django.urls import path
from .views import RegisterView, LoginView, PostView, FollowCreateView, UnfollowView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('create-post/', PostView.as_view(), name='create_post'),
    path('follow/', FollowCreateView.as_view(), name='follow'),
    path('unfollow/', UnfollowView.as_view(), name='unfollow'),
]
