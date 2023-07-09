from rest_framework import serializers

from content.models import UserPost, PostMedia, PostLikes, PostComments
from users.serializers import UserProfileSerializer


class UserPostCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['author'] = self.context['current_user']
        return UserPost.objects.create(**validated_data)

    class Meta:
        model = UserPost
        fields = ('caption', 'location', 'id', 'is_published')


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ('media_file', 'sequence_index', 'post')


class PostMediaSerializerView(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        exclude = ('post',)


class PostFeedSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer()
    media = PostMediaSerializerView(many=True)

    class Meta:
        model = UserPost
        fields = '__all__'
        include = ('media',)


class PostLikeCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['liked_by'] = self.context['current_user']
        return PostLikes.objects.create(**validated_data)

    class Meta:
        model = PostLikes
        fields = ('id', 'post',)


class PostCommentCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['commented_by'] = self.context['current_user']
        return PostComments.objects.create(**validated_data)

    class Meta:
        model = PostComments
        fields = ('id','comment', 'post',)
