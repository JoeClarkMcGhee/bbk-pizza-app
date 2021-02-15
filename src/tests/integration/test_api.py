import pytest
from django import urls
from django.contrib.auth import models as user_models
from rest_framework import status, test

pytestmark = pytest.mark.django_db


def create_user(name, password):
    return user_models.User.objects.create_user(username=name, password=password)


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
        create_user("Harry", "you're a wizard harry!")
        url = urls.reverse("users")
        response = self.client.get(url, fomat="json")

        assert response.status_code == status.HTTP_200_OK
        expected_response = {"id": 1, "username": "Harry"}
        assert dict(response.data[0]) == expected_response

    def test_list_single_user(self):
        create_user("Tony", "the tiger")
        response = self.client.get("/users/1", fomat="json")

        assert response.status_code == status.HTTP_200_OK
        expected_response = {"id": 1, "username": "Tony"}
        assert response.data == expected_response


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
