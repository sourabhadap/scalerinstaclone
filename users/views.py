from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .form import UserSignUp
from rest_framework import generics
from rest_framework import mixins


def index(request):
    # message = f"{request.method} -- {request.path} {request.META}"
    # user = User.objects.count()
    form = UserSignUp()
    errors = []

    if request.method == 'POST':
        print(request.POST)
        form = UserSignUp(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
        else:
            errors = form.errors

    context = {
        'form': form,
        'errors': errors
    }

    return render(request, 'users/index.html', context)


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)

    response = {
        "errors": None,
        "data": None
    }

    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response["data"] = {
            "success": True,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        response_status = status.HTTP_201_CREATED
    else:
        response["errors"] = serializer.errors
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(response, status=response_status)


# Functions based views
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = UserProfile.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Class based views
class UserViewDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # TODO: UPDATE THIS ENDPOINT TO RETURN USER POSTS WITH USER PROFILE - in this view
    # TODO: OR CREATE A ENDPOINT THAT RETURNS USER POSTS OF A GIVEN USER - in content views

    def get(self, request, pk=None):
        user = UserProfile.objects.filter(pk=pk).first()
        if user:
            serializer = UserProfileSerializer(user)
            response = {
                "errors": None,
                "data": serializer.data
            }
            response_status = status.HTTP_200_OK
        else:
            response = {
                "errors": "User not found",
                "data": None
            }
            response_status = status.HTTP_404_NOT_FOUND

        return Response(response, status=response_status)

    def post(self, request,pk):
        user_update_serializer = UserProfileUpdateSerializer(data=request.data, instance=request.user.profile)
        if user_update_serializer.is_valid():
            up = user_update_serializer.save()
            response = {
                "errors": None,
                "data": UserProfileSerializer(instance=up).data
            }
            response_status = status.HTTP_200_OK
        else:
            response = {
                "errors": user_update_serializer.errors,
                "data": None
            }
            response_status = status.HTTP_404_NOT_FOUND

        return Response(response, status=response_status)

    def delete(self, request, pk):
        user = request.user

        user.delete()
        response = {
            "errors": None,
            "data": "User deleted successfully"
        }
        response_status = status.HTTP_200_OK

        return Response(response, status=response_status)


class UserNetworkEdgeView(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin
                          ,generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = NetworkEdge.objects.all()
    serializer_class = UserNetworkEdgeCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            edge_direction = self.request.query_params.get("direction", None)
            if edge_direction == "followers":
                return UserNetworkEdgeFollowerViewSerializer
            elif edge_direction == "following":
                return UserNetworkEdgeFollowingViewSerializer
            return UserNetworkEdgeViewSerializer
        return self.serializer_class

    def get_queryset(self):
        edge_direction = self.request.query_params.get("direction", None)
        if edge_direction == "followers":
            return self.queryset.filter(to_user=self.request.user.profile)
        elif edge_direction == "following":
            return self.queryset.filter(from_user=self.request.user.profile)
        return NetworkEdge.objects.all()

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        request.data['from_user'] = request.user.profile.id
        return self.create(request, *args, **kwargs)

    def delete(self,request):
        network_edge = NetworkEdge.objects.filter(from_user=request.user.profile.id,to_user=request.data['to_user'])
        if network_edge.exists():
            network_edge.delete()
            response = {
                "errors": None,
                "data": "User unfollowed."
            }
            response_status = status.HTTP_200_OK
        else:
            response = {
                "errors": "User not found",
                "data": None
            }
            response_status = status.HTTP_404_NOT_FOUND
        return Response(response, status=response_status)
