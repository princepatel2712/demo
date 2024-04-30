from .serializers import UserModelSerializer, LoginSerializer, PostModelSerializer, FollowSerializer
from .models import Follow
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication


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
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class UnfollowView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        try:
            user_to_unfollow = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow).first()
        if not follow:
            return Response({'message': 'User is not followed'}, status=status.HTTP_400_BAD_REQUEST)
        follow.delete()
        return Response({'message': 'User unfollowed successfully'}, status=status.HTTP_204_NO_CONTENT)