from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["email", "password", "username"]  # order doesn't matter
        extra_kwargs = {
            "username": {"required": False, "allow_blank": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token obtain serializer to allow login with either username or email.
    """

    def validate(self, attrs):
        credentials = {
            "email": attrs.get("email"),
            "password": attrs.get("password"),
        }

        user = User.objects.filter(email__iexact=credentials["email"]).first()
        if user and user.check_password(credentials["password"]):
            refresh = self.get_token(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        raise serializers.ValidationError("Invalid email or password.")
