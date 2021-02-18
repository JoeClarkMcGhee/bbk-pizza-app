from django.contrib.auth import models as user_models
from rest_framework import serializers
from src.app.data import models


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)

    def create(self, validated_data):
        return user_models.User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )


class UsersViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = ["id", "username"]


class CreatePostSerializer(serializers.Serializer):
    expires_at = serializers.DateTimeField()
    author = serializers.PrimaryKeyRelatedField(queryset=user_models.User.objects.all())
    title = serializers.CharField(max_length=255)
    body = serializers.CharField()
    # Because we define a PrimaryKeyRelatedField on author we bind the Post model to the
    # serializer. topics is not on the Post model so we have to set the serializer type to
    # SerializerMethodField and define how we want the topics to be returned.
    topics = serializers.SerializerMethodField(method_name="get_topics")

    def get_topics(self, obj):
        return [t.topic for t in obj.topics.all()]

    def create(self, validated_data):
        return models.Post.create(
            expires_at=validated_data["expires_at"],
            author=validated_data["author"],
            title=validated_data["title"],
            body=validated_data["body"],
            # We have to get topics from the initial_data as it won't be in validated_data. Due
            # to the binding of the serializer to the Post model we only validated the fields
            # defined on the Post model.
            topics=self.initial_data["topics"],
        )


class ListPostsSerializer(serializers.ModelSerializer):
    topics = serializers.StringRelatedField(many=True)
    reactions = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Post
        fields = [
            "created_at",
            "expires_at",
            "author",
            "title",
            "body",
            "topics",
            "reactions",
        ]


class CreateReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reaction
        fields = ["created_at", "like_or_dislike", "comment", "author", "post"]
