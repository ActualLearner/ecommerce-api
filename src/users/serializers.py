from django.contrib.auth import get_user_model

User = get_user_model()
from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer,
    UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer,
)
from django.contrib.auth import get_user_model


class UserCreateSerializer(BaseUserCreatePasswordRetypeSerializer):
    class Meta(BaseUserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "password")


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name")
