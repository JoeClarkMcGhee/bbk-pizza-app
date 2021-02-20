from django.contrib.auth import models as user_models
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from src.app.interfaces.api import serializers


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer


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
        return get_object_or_404(queryset, **filter_kwargs)
