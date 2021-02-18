import io
from datetime import datetime as dt

import freezegun
import pytest
from django import urls
from django.contrib.auth import models as user_models
from rest_framework import parsers, status, test
from src.app.data import models

pytestmark = pytest.mark.django_db


def _create_user(name, password):
    return user_models.User.objects.create_user(username=name, password=password)


def _create_post(user, title, body, topics):
    models.Post.create(
        expires_at=dt.now(), author=user, title=title, body=body, topics=topics,
    )


# The test cases took significant influence from the examples on the Django Rest Framework
# documentation which can be found at https://www.django-rest-framework.org/api-guide/testing/
class TestApiEndPointsWithGoodRequests(test.APITestCase):
    def test_create_user(self):
        url = urls.reverse("create-user")
        data = {"username": "test user", "password": "pass1234"}
        response = self.client.post(url, data, fomat="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert user_models.User.objects.count() == 1
        assert response.data["id"] == 1
        assert response.data["username"] == "test user"

    def test_list_users(self):
        _create_user("Harry", "you're a wizard harry!")
        url = urls.reverse("users")
        response = self.client.get(url, fomat="json")

        assert response.status_code == status.HTTP_200_OK
        expected_response = {"id": 1, "username": "Harry"}
        assert dict(response.data[0]) == expected_response

    def test_list_single_user(self):
        _create_user("Tony", "the tiger")
        response = self.client.get("/users/1", fomat="json")

        assert response.status_code == status.HTTP_200_OK
        expected_response = {"id": 1, "username": "Tony"}
        assert response.data == expected_response

    def test_create_post(self):
        user = _create_user("Denis", "password123")
        expires_at = dt.now()
        data = {
            "expires_at": f"{expires_at}",
            "author": f"{user.id}",
            "title": "My first post",
            "body": "A really long post body",
            "topics": ["Politics"],
        }
        url = urls.reverse("create-post")
        response = self.client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["author"] == user.id
        assert response.data["title"] == "My first post"
        assert response.data["body"] == "A really long post body"
        assert response.data["topics"] == ["Politics"]

    def test_list_post(self):
        # todo: update this test to also test that reactions are shown
        user = _create_user("Another User", "passwordABC")
        _create_post(user, "body", "title", ["Tech"])
        response = self.client.get("/posts/1", fomat="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["author"] == user.id
        assert response.data["title"] == "body"
        assert response.data["body"] == "title"
        assert response.data["topics"] == ["Tech"]

    @freezegun.freeze_time("2020-01-01 00:00:00", tick=False)
    def test_list_all_posts(self):
        user = _create_user("Super cool user", "passwordXYZ")
        _create_post(user, "title A", "body A", ["Tech"])
        _create_post(user, "title B", "body B", ["Tech", "Sport"])
        url = urls.reverse("posts")
        response = self.client.get(url, fomat="json")

        assert response.status_code == status.HTTP_200_OK

        # Parsing the response byte content taken from the rest documentation.
        # https://www.django-rest-framework.org/tutorial/1-serialization/#working-with-serializers
        content = io.BytesIO(response.content)
        data = parsers.JSONParser().parse(content)

        assert data == [
            {
                "created_at": "2020-01-01T00:00:00Z",
                "expires_at": "2020-01-01T00:00:00Z",
                "author": 1,
                "title": "title A",
                "body": "body A",
                "topics": ["Tech"],
            },
            {
                "created_at": "2020-01-01T00:00:00Z",
                "expires_at": "2020-01-01T00:00:00Z",
                "author": 1,
                "title": "title B",
                "body": "body B",
                "topics": ["Tech", "Sport"],
            },
        ]


class TestApiEndPointsWithBadRequests:
    @pytest.mark.skip(reason="not yet implemented")
    def test_cant_post_comment_without_user(self):
        pass

    @pytest.mark.skip(reason="not yet implemented")
    def test_bad_data_in_post_to_post_request(self):
        pass

    @pytest.mark.skip(reason="not yet implemented")
    def test_cant_react_to_comment_without_user(self):
        pass

    @pytest.mark.skip(reason="not yet implemented")
    def test_bad_data_in_react_to_post_request(self):
        pass
