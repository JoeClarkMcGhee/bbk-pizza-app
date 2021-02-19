from rest_framework import generics
from src.app.data import models
from src.app.interfaces.api import serializers


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
