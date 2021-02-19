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

    def validate_topics(self, topics):
        if len(topics) < 1 or len(topics) > 4:
            raise serializers.ValidationError(
                "You can only provide up to a 4 topic but not less than one"
            )
        try:
            [models.TopicType(t) for t in topics]
            return topics
        except ValueError:
            raise serializers.ValidationError("Invalid topic types supplied")

    def create(self, validated_data):
        return models.Post.create(
            expires_at=validated_data["expires_at"],
            author=validated_data["author"],
            title=validated_data["title"],
            body=validated_data["body"],
            # We have to get topics from the initial_data as it won't be in validated_data, due
            # to the binding of the serializer to the Post model
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


class CreateReactionSerializer(serializers.Serializer):
    like_or_dislike = serializers.CharField()
    comment = serializers.CharField()
    author = serializers.PrimaryKeyRelatedField(queryset=user_models.User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=models.Post.objects.all())

    def validate_like_or_dislike(self, like_or_dislike):
        if not like_or_dislike:
            return like_or_dislike
        try:
            return models.LikeOrDislike(like_or_dislike).value
        except ValueError:
            raise serializers.ValidationError(
                "like_or_dislike must be Like, Dislike or empty"
            )

    def create(self, validated_data):
        return models.Reaction.objects.create(**validated_data)
