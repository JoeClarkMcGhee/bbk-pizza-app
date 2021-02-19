from rest_framework import generics
from src.app.interfaces.api import serializers


class AddReactionView(generics.CreateAPIView):
    serializer_class = serializers.CreateReactionSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
