from django.contrib.auth import models as user_models
from django.db import models


class LikeOrDislike(models.TextChoices):
    LIKE = "Like"
    DISLIKE = "Dislike"


class Reaction(models.Model):
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
    post = models.ForeignKey(
        "data.Post", on_delete=models.CASCADE, related_name="reactions"
    )

    def __str__(self):
        return f"{self.created_at} - {self.author}"

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}, id: {self.pk} created_at: {self.created_at}, "
            f"author: {self.author}, post: {self.post.pk}>"
        )

    @classmethod
    def create(cls, **kwargs):
        # When new reactions are created we want to make sure that we record the author who made
        # the reaction. We have to check this at object creation because the author field is
        # nullable.
        try:
            kwargs["author"]
        except KeyError:
            raise KeyError("You must provide a list of topics associated to the post.")

        reaction = cls(**kwargs)
        reaction.save()
        return reaction
