from . import views
from .views import *
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('like', views.PostLikeViewSet)
router.register('comment', views.PostCommentViewSet)

# Viewset routers :
# GET no params : list
# GET with params : retrieve
# POST : create
# PUT with params : update
# PATCH with params : partial_update
# DELETE with params : destroy

# Separate API endpoints for creating posts & fetching posts because SPOF.


urlpatterns = [
    path('', views.UserPostCreateView.as_view(), name='user_post_view'),
    path('media/', views.PostMediaViw.as_view(), name='post_media_view'),
    path('<int:pk>/', views.UserPostDetailUpdateView.as_view(), name='user_post_update_detail_view'),
    path('', include(router.urls)),
]
