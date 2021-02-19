from django.contrib.auth import models as user_models
from rest_framework import generics
from src.app.interfaces.api import serializers


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UsersView(generics.ListAPIView):
    serializer_class = serializers.UsersViewSerializer
    queryset = user_models.User.objects.filter(is_superuser=False, is_active=True)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class DetailUserView(generics.RetrieveAPIView):
    serializer_class = serializers.UsersViewSerializer
    queryset = user_models.User.objects.filter(is_superuser=False, is_active=True)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
