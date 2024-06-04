from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from notification.triggers import *


class UserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError({'message': 'Invalid Username or Password!'})
        return {
            'user': user
        }


class LikeSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ['post_id']

    def create(self, validated_data):
        post_id = validated_data.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError({'message': 'Post does not exist.'})
        user = self.context['request'].user
        existing_dislike = Dislike.objects.filter(user=user, post=post).first()
        if existing_dislike:
            existing_dislike.delete()
        if Like.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError({'error': 'You have already liked this post.'})
        like = Like.objects.create(user=user, post=post)
        trigger_like_notification(user.id, post_id, user.username)
        return like


class DisLikeSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()

    class Meta:
        model = Dislike
        fields = ['post_id']

    def create(self, validated_data):
        post_id = validated_data.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError({'message': 'Post does not exist.'})
        user = self.context['request'].user
        existing_like = Like.objects.filter(user=user, post=post).first()
        if existing_like:
            existing_like.delete()
        if Dislike.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError({'error': 'You have already disliked this post.'})
        dislike = Dislike.objects.create(user=user, post=post)
        return dislike


class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['post_id', 'text']

    def create(self, validated_data):
        post_id = validated_data.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError({'error': 'Post Does not exist'})
        user = self.context['request'].user
        comment = Comment.objects.create(user=user, post=post, **validated_data)
        trigger_comment_notification(post.user_id, post_id, user.username, validated_data['text'])
        return comment


class PostModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    comments = CommentSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['following']

    def create(self, validated_data):
        following_user = validated_data.get('following')
        user = self.context['request'].user
        if following_user.pk == user.pk:
            raise serializers.ValidationError({'error': 'You cannot follow yourself!'})
        already_following = Follow.objects.filter(follower=user, following=following_user).exists()
        if already_following:
            raise serializers.ValidationError({'error': 'You are already following this user.'})
        new_follower = Follow.objects.create(follower=user, following=following_user)
        trigger_follow_notification(following_user.username, user.username)
        return new_follower

    def unfollow(self):
        following_user = self.validated_data['following']
        user = self.context['request'].user
        is_following = Follow.objects.filter(follower=user, following=following_user).exists()
        if not is_following:
            raise serializers.ValidationError("You are not following this user.")
        Follow.objects.filter(follower=user, following=following_user).delete()
