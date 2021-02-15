from datetime import datetime as dt

import pytest
from django.contrib.auth import models as user_models
from src.app.data import models

pytestmark = pytest.mark.django_db


class TestModels:
    # todo: turn these into factories
    @pytest.fixture
    def user(self):
        return user_models.User.objects.create_user(
            username="Homer", password="742 Evergreen Terrace"
        )

    @pytest.fixture
    def topic(self):
        return ["Politics"]

    @pytest.fixture
    def topics(self):
        return ["Health", "Politics", "Sport"]

    @pytest.fixture
    def post(self):
        user = user_models.User.objects.create_user(
            username="Bart", password="Don't have a cow man!"
        )
        return models.Post.create(
            expires_at=dt.now(),
            author=user,
            title="A super cool post",
            body="A long post body",
            topics=["Politics"],
        )

    def test_create_post_object(self, user, topic):
        models.Post.create(
            expires_at=dt.now(),
            author=user,
            title="A super cool post",
            body="A long post body",
            topics=topic,
        )
        assert models.Post.objects.all().count() == 1

    def test_multiple_topics_save_to_post(self, user, topics):
        models.Post.create(
            expires_at=dt.now(),
            author=user,
            title="Another cool post",
            body="Some stuff about the post",
            topics=topics,
        )
        assert models.Post.objects.all().count() == 1
        assert models.Topic.objects.all().count() == 3

    def test_not_able_to_create_post_object_when_no_topic_supplied(self, user):
        with pytest.raises(KeyError):
            models.Post.create(
                expires_at=dt.now(),
                author=user,
                title="A post the shouldn't work",
                body="Good luck getting this to save!",
            )

    def test_post_not_destroyed_if_user_deleted(self, user, topic):
        post = models.Post.create(
            expires_at=dt.now(),
            author=user,
            title="A post that going to lose its author",
            body="I hope you saved the user somewhere else....",
            topics=topic,
        )
        # Test that there are no post without an author
        assert models.Post.objects.filter(author=None).count() == 0

        user.delete()
        post.refresh_from_db()

        # After we have deleted the user we expect the post to be intact but the author field to
        # be None
        assert not post.author
        assert models.Post.objects.filter(author=None).count() == 1

    def test_create_reaction(self, user, post):
        reaction = models.Reaction.create(
            like_or_dislike="Like",
            comment="A really nice comment about the post",
            author=user,
            post=post,
        )
        assert models.Reaction.objects.all().count() == 1
        assert post.reactions.get(pk=1) == reaction

    def test_not_able_to_create_reaction_if_no_author_provided(self, post):
        with pytest.raises(KeyError):
            models.Reaction.create(
                like_or_dislike="Like",
                comment="A really nice comment about the post",
                post=post,
            )
        assert models.Reaction.objects.all().count() == 0

    def test_assign_multiple_reactions_to_the_same_post(self, user, post):
        assert post.reactions.count() == 0
        # First reaction.
        models.Reaction.create(
            like_or_dislike="Like",
            comment="A really nice comment about the post",
            author=user,
            post=post,
        )
        # Second reaction
        models.Reaction.create(
            like_or_dislike="Dislike",
            comment="A not very nice post about the post",
            author=user,
            post=post,
        )
        assert post.reactions.count() == 2

    def test_reactions_are_deleted_if_post_deleted(self, user, post):
        models.Reaction.create(
            like_or_dislike="Like",
            comment="A really nice comment about the post",
            author=user,
            post=post,
        )
        models.Reaction.create(
            like_or_dislike="Dislike",
            comment="A not very nice post about the post",
            author=user,
            post=post,
        )
        # Test that the post have two reactions saved to it.
        assert post.reactions.count() == 2

        post.delete()

        # Test that the post has been deleted as well as both of the reactions.
        assert models.Post.objects.count() == 0
        assert models.Reaction.objects.count() == 0
