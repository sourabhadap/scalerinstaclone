from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

urlpatterns = [
    path('', views.index, name='users_main_index'),
    path('add/', views.create_user, name='users_create_user'),
    path('login/', TokenObtainPairView.as_view(), name='users_login'),
    path('refresh/', TokenRefreshView.as_view(), name='users_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='users_verify'),
    path('profile/', views.user_list, name='users_profile'),
    path('<int:pk>/',views.UserViewDetail.as_view(),name='users_detail_view'),
    path('edge/',views.UserNetworkEdgeView.as_view(),name='users_network_edge_create'),
]