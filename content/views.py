from django.shortcuts import render

# Create your views here.
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from content.models import PostComments,PostLikes,UserPost,PostMedia
from content.permissions import IsOwnerOrReadOnlyComment, IsOwnerOrReadOnlyLike
from content.serializers import *
from content.filters import *


class UserPostCreateView(generics.GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    queryset = UserPost.objects.all()
    serializer_class = UserPostCreateSerializer
    filter_backends = [CurrentUserFollowingFilterBackend, ]

    # TODO: CREATE A SYSTEM TO FOLLOW TOPICS,TAGS
    # TODO: ORDERING OF POSTS : POPULARITY / RECENT

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostFeedSerializer
        return self.serializer_class

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostMediaViw(generics.GenericAPIView,
                   mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    serializer_class = PostMediaSerializer

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserPostDetailUpdateView(generics.GenericAPIView,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin):
    # TODO: CREATE CELERY TASK THAT PROCESS IMAGES TO DIFFERENT SIZES

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = UserPostCreateSerializer
    queryset = UserPost.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostFeedSerializer
        return self.serializer_class

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # TODO: FILTER OUT POSTS THAT ARE NOT PUBLISHED
    # TODO: ENDPOINT TO DELETE POSTS
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PostLikeViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,IsOwnerOrReadOnlyLike,)
    authentication_classes = (JWTAuthentication,)
    queryset = PostLikes.objects.all()
    serializer_class = PostLikeCreateSerializer

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}

    # TODO: IMPLEMENT SERIALIZER FOR POST LIKED BY USER PROFILE
    # TODO: UPDATE FEED SERIALIZER TO CARRY LIKES COUNT
    # TODO: UPDATE POST DETAIL SERIALIZER TO SHOW LIKES COUNT

    # TODO: CREATE NOTIFICATION SYSTEM TO NOTIFY USERS WHEN THEIR POSTS ARE LIKED
    def list(self,request):
        post_likes = self.queryset.filter(post_id=request.query_params.get('post_id'))
        page = self.paginate_queryset(post_likes)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(post_likes, many=True)
        return Response(serializer.data)


class PostCommentViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyComment,)
    authentication_classes = (JWTAuthentication,)
    queryset = PostComments.objects.all()
    serializer_class = PostCommentCreateSerializer

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}

    # TODO: IMPLEMENT SERIALIZER FOR POST LIKED BY USER PROFILE
    # TODO:  SHOW ALL COMMENTS ON POST DETAIL VIEW
    def list(self, request):
        post_comments = self.queryset.filter(post_id=request.query_params.get('post_id'))
        page = self.paginate_queryset(post_comments)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(post_comments, many=True)
        return Response(serializer.data)