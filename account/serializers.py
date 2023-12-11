from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers

from account.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        extra_kwargs = {
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
            "is_active": {"read_only": True},
            "date_joined": {"read_only": True},
            "last_login": {"read_only": True},
        }
        exclude = ("groups", "user_permissions")

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        user = get_user_model().objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.date_joined = timezone.now()
        user.save()

        for key, value in profile_data.items():
            setattr(user.profile, key, value)
        user.profile.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64)


class LogoutSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)


class RequestResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_new_password(new_password):
        validate_password(new_password)
        return new_password


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_new_password(data):
        validate_password(data)
        return data
