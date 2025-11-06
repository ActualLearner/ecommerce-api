from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer

User = get_user_model()
# Create your views here.


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = []

    def perform_create(self, serializer):
        # The parent method creates the user and sends the activation email.
        user = serializer.save()

        # After the user is created, we add the user object to the view's instance.
        # This makes it available for the response.
        # This is a bit of a "blessed hack" recommended by Djoser's customization patterns.
        self.instance = user

    # The create method is what generates the final response.
    # We override it to use our new `self.instance`.
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Use the standard 'user' serializer (not the create one) to format the output.
        read_serializer = self.get_serializer(self.instance)

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
