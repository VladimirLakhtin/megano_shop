import json

from django.contrib.auth import authenticate, login, logout
from rest_framework import status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from accounts.serializers import (
    ProfileSerializer,
    UpdatePasswordSerializer,
    CreateUserSerializer,
    AvatarSerializer,
)


class SignInView(APIView):
    """User login view"""

    def post(self, request: Request) -> Response:
        user_data = json.loads(list(request.POST.keys())[0])
        username = user_data.get("username")
        password = user_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    """View for user registration"""

    def post(self, request: Request) -> Response:
        user_data = json.loads(list(request.POST.keys())[0])
        user_data["first_name"] = user_data.get("name")
        serializer = CreateUserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            user = authenticate(
                request,
                username=user_data.get("username"),
                password=user_data.get("password"),
            )
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignOutView(APIView):
    """Logout user view"""

    def post(self, request: Request) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ProfileDetailsView(APIView):
    """View for get user profile and update user info"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(APIView):
    """View for update user password"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        user = request.user
        serializer = UpdatePasswordSerializer(
            instance=user,
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAvatarView(APIView):
    """View for update user avatar"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        user = request.user
        profile = Profile.objects.get(user=user)
        avatar_file = request.FILES.get("avatar", None)
        serializer = AvatarSerializer(data={"src": avatar_file})
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
