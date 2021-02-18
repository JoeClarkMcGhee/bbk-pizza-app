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
    post = models.ForeignKey(
        "data.Post", on_delete=models.CASCADE, related_name="topics"
    )

    def __str__(self):
        return f"{self.topic}"

    def __repr__(self):
        return f"<{self.__class__.__name__}, id: {self.pk} topic: {self.topic}>"
