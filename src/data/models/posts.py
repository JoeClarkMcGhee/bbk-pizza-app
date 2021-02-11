from django.contrib.auth import models as user_models
from django.db import models


class Posts(models.Model):
    """
    Model for storing user posts.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    # on_delete kwarg set to SET_NULL such that, if a user is deleted, the post remains intact.
    author = models.ForeignKey(user_models.User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
