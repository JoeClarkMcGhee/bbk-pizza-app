from django.contrib.auth import models as user_models
from rest_framework import generics

from ...data import models
from . import serializers


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


class CreatePostView(generics.CreateAPIView):
    serializer_class = serializers.CreatePostSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PostsView(generics.ListAPIView):
    serializer_class = serializers.ListPostsSerializer
    queryset = models.Post.objects.all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class DetailPostView(generics.RetrieveAPIView):
    serializer_class = serializers.ListPostsSerializer
    queryset = models.Post.objects.all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AddReactionView(generics.CreateAPIView):
    serializer_class = serializers.CreateReactionSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
