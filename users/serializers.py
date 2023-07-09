from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth.hashers import make_password


class UserSerializer(ModelSerializer):

    def create(self, validated_data):

        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        UserProfile.objects.create(user=user)
        return user

    class Meta:
        model = User
        fields = '__all__'


class UserViewSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class UserProfileSerializer(ModelSerializer):
    user = UserViewSerializer()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


class UserProfileUpdateSerializer(ModelSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def update(self, instance, validated_data):
        user = instance.user
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']

        user.save()
        instance.bio = validated_data['bio']
        instance.profile_pic = validated_data['profile_pic']
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','bio','profile_pic')


class UserNetworkEdgeCreateSerializer(ModelSerializer):

    class Meta:
        model = NetworkEdge
        fields = ('from_user','to_user')


class UserNetworkEdgeViewSerializer(ModelSerializer):

    from_user = UserProfileSerializer()
    to_user = UserProfileSerializer()

    class Meta:
        model = NetworkEdge
        fields = '__all__'


class UserNetworkEdgeFollowerViewSerializer(ModelSerializer):

    from_user = UserProfileSerializer()

    class Meta:
        model = NetworkEdge
        fields = ('from_user',)


class UserNetworkEdgeFollowingViewSerializer(ModelSerializer):

    to_user = UserProfileSerializer()

    class Meta:
        model = NetworkEdge
        fields = ('to_user',)
