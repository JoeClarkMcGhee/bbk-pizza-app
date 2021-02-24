import requests
from django.conf import settings
from django.contrib.auth import models as user_models
from rest_framework import generics, permissions, response, status, views
from src.app.interfaces.api import serializers


class Token(views.APIView):
    """
    Get tokens with username and password.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        r = requests.post(
            settings.TOKEN_URL,
            data={
                "grant_type": "password",
                "username": request.data["username"],
                "password": request.data["password"],
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
            },
        )
        return response.Response(r.json())


class CreateUserView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CreateUserSerializer

    def post(self, request, *args, **kwargs):
        user = self.create(request, *args, **kwargs)
        token = requests.post(
            settings.TOKEN_URL,
            data={
                "grant_type": "password",
                "username": request.data["username"],
                "password": request.data["password"],
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
            },
        )
        data = token.json()
        data.update(user.data)
        return response.Response(data=data, status=status.HTTP_201_CREATED)


class UsersView(generics.ListAPIView):
    serializer_class = serializers.UsersViewSerializer
    queryset = user_models.User.objects.filter(is_superuser=False, is_active=True)


class DetailUserView(generics.RetrieveAPIView):
    serializer_class = serializers.UsersViewSerializer
    queryset = user_models.User.objects.filter(is_superuser=False, is_active=True)


class DetailUserViewByName(generics.RetrieveAPIView):
    serializer_class = serializers.UsersViewSerializer
    queryset = user_models.User.objects.filter(is_superuser=False, is_active=True)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"username": self.kwargs["username"]}
        return generics.get_object_or_404(queryset, **filter_kwargs)
