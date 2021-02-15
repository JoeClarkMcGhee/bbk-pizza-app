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
        # todo: parse the datetime to a date
        return f"{self.created_at} - {self.title}"

    def __repr__(self):
        # todo: test the __repr__
        return (
            f"<{self.__class__.__name__}, id: {self.pk} created_at: {self.created_at}, "
            f"expires_at: {self.expires_at}, title: {self.title}>"
        )

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs):
        """
        Custom create method that ensures at least one topic is assocaited to a post.
        """
        # Check that topics have been supplied.
        try:
            topics_to_save = kwargs.pop("topics")
        except KeyError:
            raise KeyError("You must provide a list of topics associated to the post.")

        # Check they are of the correct type for us to operate on.
        if type(topics_to_save) is not list:
            raise ValueError("You must provide topics as a list")

        #  Check for an empty or over sized list.
        if len(topics_to_save) < 1 or len(topics_to_save) > 4:
            raise ValueError("You must provide at least 1 topic but no more than 4")

        # Validate that the topic type is legal.
        try:
            [topic_model.TopicType(t) for t in topics_to_save]
        except ValueError:
            raise ValueError("Invalid topic types supplied")

        # At this stage we are happy that the supplied topics are valid so we can save the post
        post = cls(**kwargs)
        post.save()

        # And then save the topics. We save the topics after the post as the topics have a
        # foreign key to the post.
        for topic in set(topics_to_save):
            topic_model.Topic.objects.create(topic=topic, post=post)

        return post
