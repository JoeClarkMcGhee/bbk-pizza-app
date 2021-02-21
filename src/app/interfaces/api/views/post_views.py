from rest_framework import generics, response
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


class PostsByTopicView(generics.ListAPIView):
    queryset = models.Topic.objects.all()
    serializer_class = serializers.ListPostsSerializer

    # The list method defined bellow was influenced by the following section in the django rest
    # framework documentation.
    # https://www.django-rest-framework.org/api-guide/generic-views/#examples
    def list(self, request, *args, **kwargs):
        post_ids = [
            topic.post.id for topic in self.get_queryset().filter(topic=kwargs["topic"])
        ]
        queryset = models.Post.objects.filter(id__in=post_ids)
        serializer = serializers.ListPostsSerializer(queryset, many=True)
        return response.Response(serializer.data)
