from .serializers import UserModelSerializer, LoginSerializer, PostModelSerializer, FollowSerializer, LikeSerializer, \
    DisLikeSerializer, CommentSerializer
from .models import Follow, Like, Post, Dislike, Comment
from rest_framework_simplejwt.tokens import AccessToken
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
    authentication_classes = [BasicAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def perform_create(self, serializer):
        post_id = serializer.validated_data.get('post_id')
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise ValidationError({'error': 'Post does not exist.'})
        user = self.request.user
        existing_dislike = Dislike.objects.filter(user=user, post=post).first()
        if existing_dislike:
            existing_dislike.delete()
        if Like.objects.filter(user=user, post=post).exists():
            raise ValidationError({'error': 'You have already liked this post.'})
        serializer.save(user=user, post=post)


class DislikeView(generics.CreateAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DisLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def perform_create(self, serializer):
        post_id = serializer.validated_data.get('post_id')
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise ValidationError({'error': 'Post does not exist.'})
        user = self.request.user
        existing_like = Like.objects.filter(user=user, post=post).first()
        if existing_like:
            existing_like.delete()
        if Dislike.objects.filter(user=user, post=post).exists():
            raise ValidationError({'error': 'You have already disliked this post.'})
        serializer.save(user=user, post=post)


class CommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def perform_create(self, serializer):
        post_id = serializer.validated_data.get('post_id')
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise ValidationError({'error': 'Post does not exist.'})
        if Comment.objects.filter(user=self.request.user, post=post).exists():
            raise ValidationError({'error': 'You have already commented on this post.'})
        serializer.save(user=self.request.user, post=post)


class FollowCreateView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def perform_create(self, serializer):
        following_user = serializer.validated_data.get('following')
        if following_user == self.request.user:
            raise ValidationError("You cannot follow yourself.")
        already_following = Follow.objects.filter(follower=self.request.user, following=following_user).exists()
        if already_following:
            raise ValidationError("You are already following this user.")
        serializer.save(follower=self.request.user)


class UnfollowView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def destroy(self, request, *args, **kwargs):
        user = request.user
        user_to_unfollow_id = kwargs.get('user_id')
        if user.id == int(user_to_unfollow_id):
            return Response({'error': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            follow_instance = Follow.objects.get(follower=user.id, following=user_to_unfollow_id)
        except Follow.DoesNotExist:
            return Response({'error': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)
        follow_instance.delete()
        return Response({'message': 'Unfollowed successfully.'}, status=status.HTTP_200_OK)
