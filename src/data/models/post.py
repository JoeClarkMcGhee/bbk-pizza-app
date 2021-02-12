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
        return f"{self.created_at} - {self.title}"

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}, id: {self.pk} created_at: {self.created_at}, "
            f"expires_at: {self.expires_at}, title: {self.title}>"
        )

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        Custom save method that ensures we save at least one topic to a post.
        """
        topics_to_save = kwargs.get("topics")

        # Check that topics have been supplied.
        if not topics_to_save:
            raise ValueError(
                "You must provide a list of topics associated to the post."
            )

        # Check they are of the correct type for us to operate on.
        if type(topics_to_save) is not list:
            raise ValueError("You must provide topics as a list")

        #  Check for an empty or over sized list.
        if len(topics_to_save) < 1 or len(topics_to_save) > 4:
            raise ValueError("You must provide at least 1 topic but no more than 4")

        # Validate that the topic type is legal.
        try:
            [topic.TopicType(topic) for topic in topics_to_save]
        except ValueError as e:
            raise Exception("Invalid topic types supplied") from e

        # At this stage we are happy that the supplied topics are valid so we can save the post
        post = super().save(*args, **kwargs)

        # And then save the topics. We save the topics after the post as the topics have a
        # foreign key to the post.
        for topic in set(topics_to_save):
            t = topic_model.Topic(topic=topic, post=post)
            t.save()
