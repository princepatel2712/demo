from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


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


class DisLikeSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()

    class Meta:
        model = Dislike
        fields = ['post_id']


class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['post_id', 'text']


class PostModelSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        exclude = ['user']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['following']
