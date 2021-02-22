from rest_framework import generics, response
from src.app.data import models
from src.app.interfaces.api import serializers


class CreatePostView(generics.CreateAPIView):
    serializer_class = serializers.CreatePostSerializer


class PostsView(generics.ListAPIView):
    serializer_class = serializers.ListPostsSerializer
    queryset = models.Post.objects.all()


class DetailPostView(generics.RetrieveAPIView):
    serializer_class = serializers.ListPostsSerializer
    queryset = models.Post.objects.all()


class PostsByTopicView(generics.ListAPIView):
    queryset = models.Topic.objects.all()
    serializer_class = serializers.ListPostsSerializer

    # The list method defined bellow was influenced by the following section in the django rest
    # framework documentation.
    # https://www.django-rest-framework.org/api-guide/generic-views/#examples
    def list(self, request, *args, **kwargs):
        # Get all the posts relating to a particular topic.
        post_ids = [
            topic.post.id for topic in self.get_queryset().filter(topic=kwargs["topic"])
        ]
        queryset = models.Post.objects.filter(id__in=post_ids)
        # if "expired=true" has been passed in the URL then update the queryset to return only
        # the expired posts.
        if bool(request.GET.get("expired")):
            expired_post_ids = [post.id for post in queryset if post.is_expired]
            queryset = models.Post.objects.filter(id__in=expired_post_ids)
        serializer = serializers.ListPostsSerializer(queryset, many=True)
        return response.Response(serializer.data)
