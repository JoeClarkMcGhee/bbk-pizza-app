from datetime import datetime as dt

import pytz
from django.contrib.auth import models as user_models
from django.db import models, transaction

from . import topic as topic_model


class Post(models.Model):
    """
    Model for storing user posts.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    # on_delete kwarg set to SET_NULL such that, if a user is deleted, the post remains intact.
    author = models.ForeignKey(user_models.User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return f"{self.created_at.date()} - {self.title}"

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}, id: {self.pk} created_at: {self.created_at}, "
            f"expires_at: {self.expires_at}, title: {self.title}>"
        )

    @property
    def is_expired(self):
        now = dt.now().replace(tzinfo=pytz.UTC)
        post_expires_at = self.expires_at.replace(tzinfo=pytz.UTC)
        return now > post_expires_at

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs):
        # We save the topics associated with a post at the same time as post instantiation.
        topics_to_save = kwargs.pop("topics")
        post = cls(**kwargs)
        post.save()
        for topic in set(topics_to_save):
            topic_model.Topic.objects.create(topic=topic, post=post)
        return post
