from datetime import datetime as dt

import pytest
from django.contrib.auth import models as user_models
from src.app.data import models

pytestmark = pytest.mark.django_db


class TestModels:
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

    def test_create_post_object(self, user, topic):
        """
        We test that we can create a post object
        """
        models.Post.create(
            expires_at=dt.now(),
            author=user,
            title="A super cool post",
            body="A long post body",
            topics=topic,
        )

    # def test_multiple_topics_save_to_post(self):
    #     """
    #     """
    #     pass
    #
    # def test_not_able_to_create_post_object_when_no_topic_supplied(self):
    #     """
    #     """
    #     pass
    #
    #
    # def test_create_reaction(self):
    #     """
    #     """
    #     pass
    #
    # def test_assign_multiple_reactions_to_the_same_post(self):
    #     """
    #     """
    #     pass
    #
    # def test_not_able_to_create_reaction_object_when_no_post_supplied(self):
    #     """
    #     """
    #     pass
