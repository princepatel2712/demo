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


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostModelSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PostModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return Post.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'message': 'You do not have permission to edit this post.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


class LikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]


class DislikeView(generics.CreateAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DisLikeSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class FollowCreateView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]


class UnfollowView(generics.GenericAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.unfollow()
        return Response({'message': 'Unfollowed successfully.'}, status=status.HTTP_204_NO_CONTENT)


class ListOwnFollower(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(following=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        follower_name = [follow.follower.username for follow in queryset]
        return Response({'followers-username': follower_name})


class ListOwnFollowing(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(follower=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        follower_name = [follow.following.username for follow in queryset]
        return Response({'following-username': follower_name})
