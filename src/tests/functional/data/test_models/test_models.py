from datetime import datetime as dt

import pytest
from django.contrib.auth import models as user_models
from src.app.data import models

pytestmark = pytest.mark.django_db


class TestPost:
    @pytest.fixture
    def user(self):
        return user_models.User(username="Homer", password="742 Evergreen Terrace")

    def test_create_post_object(self, user):
        """
        """
        models.Post(expires_at=dt.now(), author=user.id, title=None, body=None)

    def test_multiple_topics_save_to_post(self):
        """
        """
        pass

    def test_not_able_to_create_post_object_when_no_topic_supplied(self):
        """
        """
        pass


class TestReaction:
    def test_create_reaction(self):
        """
        """
        pass

    def test_assign_multiple_reactions_to_the_same_post(self):
        """
        """
        pass

    def test_not_able_to_create_reaction_object_when_no_post_supplied(self):
        """
        """
        pass
