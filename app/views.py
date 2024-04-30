from .serializers import UserModelSerializer, LoginSerializer, PostModelSerializer, FollowSerializer, UnfollowSerializer
from .models import Follow
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.serializers import ValidationError


class RegisterView(generics.CreateAPIView):
    serializer_class = UserModelSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print('mail sent fun')
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'User registered successfully'}, status=201)


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            access_token = AccessToken.for_user(user)
            return Response({'access_token': str(access_token)}, status=status.HTTP_200_OK)
        return Response({'message': 'Enter Valid username or password'}, status=status.HTTP_400_BAD_REQUEST)


class PostView(generics.CreateAPIView):
    serializer_class = PostModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FollowCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def perform_create(self, serializer):
        following_user = serializer.validated_data.get('following')
        if following_user == self.request.user:
            raise ValidationError("You cannot follow yourself.")
        already_following = Follow.objects.filter(
            follower=self.request.user,
            following=following_user
        ).exists()
        if already_following:
            raise ValidationError("You are already following this user.")
        serializer.save(follower=self.request.user)


class UnfollowCreateView(generics.CreateAPIView):
    serializer_class = UnfollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        following_id = serializer.validated_data['following']
        if following_id == self.request.user.id:
            raise ValidationError("You cannot unfollow yourself.")
        if not Follow.objects.filter(follower=self.request.user, following_id=following_id).exists():
            raise ValidationError("You are not following this user.")
        serializer.save(follower=self.request.user)
