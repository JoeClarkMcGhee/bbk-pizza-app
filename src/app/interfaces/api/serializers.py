from datetime import datetime as dt

import pytz
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


class CreatePostSerializer(serializers.ModelSerializer):
    # topics is not on the Post model so we have to set the serializer type to
    # SerializerMethodField and define how we want the topics to be returned.
    topics = serializers.SerializerMethodField(method_name="get_topics")

    class Meta:
        model = models.Post
        fields = ["id", "expires_at", "author", "title", "body", "topics"]

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
            # to the binding of the serializer to the Post model. This is not an issue as we
            # validate the topics in the validate_topics method above.
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
    author = serializers.PrimaryKeyRelatedField(queryset=user_models.User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=models.Post.objects.all())

    class Meta:
        model = models.Reaction
        fields = ["created_at", "like_or_dislike", "comment", "author", "post"]

    def validate_like_or_dislike(self, like_or_dislike):
        if not like_or_dislike:
            return like_or_dislike
        try:
            return models.LikeOrDislike(like_or_dislike).value
        except ValueError:
            raise serializers.ValidationError(
                "like_or_dislike must be Like, Dislike or empty"
            )

    def validate(self, data):
        # The solution to ensuring that the dates are tz aware was from the SO post bellow.
        # https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
        now = dt.now().replace(tzinfo=pytz.UTC)
        post_expires_at = data["post"].expires_at.replace(tzinfo=pytz.UTC)
        if now > post_expires_at:
            raise serializers.ValidationError(
                "This post is no long accepting reactions"
            )
        return data

    def create(self, validated_data):
        return models.Reaction.objects.create(**validated_data)
