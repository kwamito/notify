from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import mixins, generics
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserValidateSerializer, ProfileSerializer
from rest_framework import status
from .models import User, Profile
from django.http import Http404
from django.contrib.auth.hashers import check_password


# Create your views here.
class UserCreate(APIView):
    def post(self, request, format="json"):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.get(user=user)

                json = serializer.data
                json["token"] = token.__str__()
                return Response(json, status=status.HTTP_201_CREATED)
        elif serializer.is_valid() != True:
            if len(serializer.data["email"]) < 8:
                json = serializer.data
                json["error"] = "Password should be more than 8 characters long"
                return Response()
            if User.objects.get(email=serializer.data["email"]) == True:
                json = serializer.data
                json[
                    "error"
                ] = "User already exists if you already have an account, login"
                return Response(json, status=status.HTTP_401_UNAUTHORIZED)

        else:
            json = serializer.data
            json["error"] = "Unknown error"
            return Response(json, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    def post(self, request, format="json"):
        user_email = request.data["email"]
        user_password = request.data["password"]
        user = User.objects.get(email=user_email)
        checker = check_password(user_password, user.password)
        if checker is not False:
            token = Token.objects.get(user=user)
            response = token.__str__()
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = "Wrong password or username"
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # serializer_class = UserValidateSerializer
        serializer = self.serializer_class(
            data=request.data, context={"request", request}
        )
        # serializer = serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["email"]
        token, created = Token.objects.get_or_create(user=user)
        print(token)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class ProfileApiView(APIView):
    def get_object(self, user):
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user = request.user
        profile = self.get_object(user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, format=None):
        user = request.user
        profile = self.get_object(user)
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(instance=profile, validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
