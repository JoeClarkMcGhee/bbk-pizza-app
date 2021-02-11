from django.contrib.auth import models as user_models
from django.db import models

from . import posts


class LikeOrDislike(models.TextChoices):
    LIKE = "Like"
    DISLIKE = "Dislike"


class Reactions(models.Model):
    """
    A model to store user reactions associated with a Post instance.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    like_or_dislike = models.CharField(
        choices=LikeOrDislike.choices, max_length=255, null=True, blank=True
    )
    comment = models.TextField(null=True, blank=True)
    # on_delete set to SET_NULL such that, if a user is deleted, the post remains intact.
    author = models.ForeignKey(user_models.User, on_delete=models.SET_NULL, null=True)
    # on_delete set to CASCADE such that, if a post is deleted, all the comments associated to
    # that post are deleted too.
    post = models.ForeignKey(posts.Posts, on_delete=models.CASCADE)
