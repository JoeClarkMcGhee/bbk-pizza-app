from django.db import models


class TopicType(models.TextChoices):
    POLITICS = "Politics"
    HEALTH = "Health"
    SPORT = "Sport"
    TECH = "Tech"


class Topic(models.Model):
    """
    A model to store the topics associated to a post.
    """

    topic = models.CharField(max_length=255, choices=TopicType.choices)
    # on_delete set to CASCADE such that, if a post is deleted, all the topics associated to
    # that post are deleted too.
    post = models.ForeignKey("data.Post", on_delete=models.CASCADE)
