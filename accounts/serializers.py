import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"]
        )


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "User account is inactive."
            )

        attrs["user"] = user

        return attrs

class RefreshTokenSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs["refresh"]

        try:
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError(
                "Refresh token has expired."
            )

        except jwt.InvalidTokenError:
            raise serializers.ValidationError(
                "Invalid refresh token."
            )

        if payload.get("type") != "refresh":
            raise serializers.ValidationError(
                "Invalid token type."
            )

        user_id = payload.get("user_id")

        if not user_id:
            raise serializers.ValidationError(
                "Invalid token payload."
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User not found."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "User account is inactive."
            )

        attrs["user"] = user

        return attrs