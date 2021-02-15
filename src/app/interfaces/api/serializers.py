from django.contrib.auth import models as user_models
from rest_framework import serializers


class CreateUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
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
