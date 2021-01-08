from .filters import DoctorFilter
from requests.models import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import UpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsOwner
from .serializers import (
    CustomTokenObtainPairSerializer, RegisterSerializer, ChangePasswordSerializer)

from django.shortcuts import render, get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ProfileSerializer, ProfileSerializerPut
from .models import Doctor, User, Profile, UserType


def get_user_by_type(user):
    print(UserType[user.get_user_type_display()].value, user.id)
    user_type = UserType[user.get_user_type_display()].value
    return get_object_or_404(user_type, user_id=user.id)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegisterSerializer

    def post(self, request):
        user = User(email=self.request.user)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogoutApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer


class HelloWorldView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"hello": "world"}, status=status.HTTP_200_OK)


class ProfileAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user: User = request.user
        profile_serializer = ProfileSerializer(get_user_by_type(user))
        data = profile_serializer.data
        data["number_of_requests"] = len(user.incoming_requests.all())
        return Response(data)

    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        profile_serializer = ProfileSerializerPut(user.profile, data=data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user: User = request.user
        user.delete()
        return Response({"detail": "Successful"}, status=status.HTTP_200_OK)


class DoctorList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.all()
        filters = DoctorFilter(request.GET, queryset=doctors)
        return Response(ProfileSerializer(filters.qs, many=True).data)
