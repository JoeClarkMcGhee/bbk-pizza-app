from django.http import Http404
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


class HighestInterestPost(generics.RetrieveAPIView):
    serializer_class = serializers.ListPostsSerializer
    queryset = models.Topic.objects.all()

    def get_object(self):
        # Get all the posts relating to a particular topic.
        post_ids = [
            topic.post.id
            for topic in self.get_queryset().filter(topic=self.kwargs["topic"])
        ]
        queryset = models.Post.objects.filter(id__in=post_ids)

        # Check if the user just wants active posts
        if self.request.GET.get("active") == "true":
            return self.get_active_highest_interest(queryset)
        # Else, query against all posts.
        return self.get_all_time_highest_interest(queryset)

    def get_all_time_highest_interest(self, queryset):
        if queryset.count() < 0:
            raise Http404("No posts for topic")

        post_with_most_reactions = queryset.objects.first()
        for post in queryset:
            if post.reactions.count() >= post_with_most_reactions.reactions.count():
                post_with_most_reactions = post

        return post_with_most_reactions

    def get_active_highest_interest(self, queryset):

        active_posts = [post for post in queryset if not post.is_expired]

        if len(active_posts) < 0:
            raise Http404("No active posts for topic")

        post_with_most_reactions = active_posts[0]
        for post in active_posts:
            if post.reactions.count() >= post_with_most_reactions.reactions.count():
                post_with_most_reactions = post

        return post_with_most_reactions


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
        # if "active=false" has been passed in the URL then update the queryset to return only
        # the expired posts.
        if request.GET.get("active") == "false":
            expired_post_ids = [post.id for post in queryset if post.is_expired]
            queryset = models.Post.objects.filter(id__in=expired_post_ids)
        serializer = serializers.ListPostsSerializer(queryset, many=True)
        return response.Response(serializer.data)
