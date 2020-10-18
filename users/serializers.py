from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.conf import settings
from .models import User, Profile, Follow
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)
    avatar = serializers.ReadOnlyField(source="profile_image")

    def create(self, validated_data):
        user = User.objects._create_user(
            validated_data["email"], validated_data["password"], False, False
        )
        return user

    class Meta:
        model = User
        fields = ("id", "email", "password", "avatar")


class UserValidateSerializer(serializers.ModelSerializer):
    def validate(self, validated_data):
        print("Validated data is {}".format(validated_data))
        user = User.objects.get(email=validated_data["email"])
        token = Token.objects.get(user=user)
        return token

    class Meta:
        model = User
        fields = ("id", "email", "password")


class FollowSerializer(serializers.ModelSerializer):
    follower_count = serializers.ReadOnlyField(source="followers_count")
    follower_image = serializers.ReadOnlyField(source="follower.profile.image_url")
    follower = serializers.ReadOnlyField(source="follower.profile.user.email")

    class Meta:
        model = Follow
        fields = (
            "follower",
            "following",
            "created",
            "follower_count",
            "follower_image",
        )


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="user.email")
    ident = serializers.ReadOnlyField(source="user.id")
    notes_count = serializers.ReadOnlyField(source="user_notes_count")
    follower_count = serializers.ReadOnlyField(source="followers_count")
    followers = FollowSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "email",
            "bio",
            "image_url",
            "notes_count",
            "follower_count",
            "followers",
        )


class ProfileFollowSerializer(serializers.ModelSerializer):
    followers = FollowSerializer()
    profile = ProfileSerializer()

    class Meta:
        fields = ("bio", "follower", "created")
