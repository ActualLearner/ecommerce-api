from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()
# Create your views here.


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = []


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for token creation that uses our custom serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer
