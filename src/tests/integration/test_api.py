from datetime import datetime as dt

import freezegun
import pytest
from django import urls
from django.contrib.auth import models as user_models
from rest_framework import status, test
from src.app.data import models
from src.app.interfaces.api.views import post_views, reaction_views, user_views

pytestmark = pytest.mark.django_db


def _create_user(name, password):
    return user_models.User.objects.create_user(username=name, password=password)


def _create_post(user, title, body, topics):
    return models.Post.create(
        expires_at=dt.now(), author=user, title=title, body=body, topics=topics,
    )


# The test cases took influence from the examples on the Django Rest Framework documentation
# which can be found at https://www.django-rest-framework.org/api-guide/testing/
class TestApiEndPointsWithGoodRequests(test.APITestCase):
    factory = test.APIRequestFactory()

    def test_create_user(self):
        url = urls.reverse("create-user")
        data = {"username": "testuser", "password": "pass1234"}
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert user_models.User.objects.count() == 1
        assert response.data["username"] == "testuser"

    def test_list_users(self):
        user = _create_user("Harry", "you're a wizard harry!")
        url = urls.reverse("users")
        request = self.factory.get(url, format="json")
        test.force_authenticate(request, user=user)
        response = user_views.UsersView.as_view()(request)

        assert response.status_code == status.HTTP_200_OK
        expected_response = {"id": 1, "username": "Harry"}
        assert dict(response.data[0]) == expected_response

    def test_list_single_user(self):
        user = _create_user("Tony", "the tiger")
        request = self.factory.get(path="/users/1")
        test.force_authenticate(request, user=user)
        view = user_views.DetailUserView.as_view()
        response = view(request, pk=1)

        assert response.status_code == status.HTTP_200_OK
        expected_response = {"id": 1, "username": "Tony"}
        assert response.data == expected_response

    def test_get_user_by_name(self):
        user = _create_user("Tony", "the tiger")
        request = self.factory.get(path="/users/Tony")
        test.force_authenticate(request, user=user)
        view = user_views.DetailUserViewByName.as_view()
        response = view(request, username="Tony")

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
        request = self.factory.post(url, data=data)
        test.force_authenticate(request, user=user)
        view = post_views.CreatePostView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["author"] == user.id
        assert response.data["title"] == "My first post"
        assert response.data["body"] == "A really long post body"

    def test_list_post(self):
        user = _create_user("AnotherUser", "passwordABC")
        _create_post(user, "body", "title", ["Tech"])
        request = self.factory.get("/posts/1")
        test.force_authenticate(request, user=user)
        view = post_views.DetailPostView.as_view()
        response = view(request, pk=1)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["author"] == user.id
        assert response.data["title"] == "body"
        assert response.data["body"] == "title"
        assert response.data["topics"] == ["Tech"]

    @freezegun.freeze_time("2020-01-01 00:00:00", tick=False)
    def test_list_all_posts(self):
        user = _create_user("SuperCoolUser", "passwordXYZ")
        _create_post(user, "title A", "body A", ["Tech"])
        _create_post(user, "title B", "body B", ["Tech", "Sport"])
        url = urls.reverse("posts")
        request = self.factory.get(url)
        test.force_authenticate(request, user=user)
        view = post_views.PostsView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                "created_at": "2020-01-01T00:00:00Z",
                "expires_at": "2020-01-01T00:00:00Z",
                "author": 1,
                "reactions": [],
                "title": "title A",
                "body": "body A",
                "topics": ["Tech"],
            },
            {
                "created_at": "2020-01-01T00:00:00Z",
                "expires_at": "2020-01-01T00:00:00Z",
                "author": 1,
                "reactions": [],
                "title": "title B",
                "body": "body B",
                "topics": ["Sport", "Tech"],
            },
        ]

    @freezegun.freeze_time("2020-01-01 00:00:00", tick=False)
    def test_add_reactions_to_post(self):
        post_author = _create_user("CoolDudeUser", "password1234")
        post = _create_post(post_author, "title", "body", ["Tech", "Sport", "Politics"])
        user = _create_user("CoolDude", "password1234")

        # Add the first reaction.
        url = urls.reverse("add-reaction")
        first_reaction = {
            "like_or_dislike": "Like",
            "comment": "I really like this post",
            "author": user.id,
            "post": post.id,
        }
        request = self.factory.post(url, data=first_reaction)
        test.force_authenticate(request, user=user)
        view = reaction_views.AddReactionView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["like_or_dislike"] == "Like"
        assert response.data["author"] == user.id
        assert response.data["post"] == post.id

        # Add the second reaction.
        second_reaction = {
            "like_or_dislike": "Dislike",
            "comment": "not for me",
            "author": user.id,
            "post": post.id,
        }
        request = self.factory.post(url, data=second_reaction)
        test.force_authenticate(request, user=user)
        view = reaction_views.AddReactionView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["like_or_dislike"] == "Dislike"
        assert response.data["author"] == user.id
        assert response.data["post"] == post.id

        # We then test that the reactions have been added to the post and that they are return
        # correctly when we hit the post-detail end point.
        request = self.factory.get("/posts/1")
        test.force_authenticate(request, user=user)
        view = post_views.DetailPostView.as_view()
        response = view(request, pk=1)

        assert response.data == {
            "created_at": "2020-01-01T00:00:00Z",
            "expires_at": "2020-01-01T00:00:00Z",
            "author": 1,
            "reactions": [
                "2020-01-01 - CoolDude - Like - I really like this post",
                "2020-01-01 - CoolDude - Dislike - not for me",
            ],
            "title": "title",
            "body": "body",
            "topics": ["Politics", "Sport", "Tech"],
        }


class TestApiEndPointsWithBadRequests:
    @pytest.mark.skip(reason="not yet implemented")
    def test_cant_post_comment_without_user(self):
        pass

    @pytest.mark.skip(reason="not yet implemented")
    def test_cant_post_reaction_if_not_valid_user(self):
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
