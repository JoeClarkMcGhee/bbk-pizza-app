import io
from datetime import datetime as dt

import freezegun
import pytest
from django import urls
from rest_framework import parsers, status, test


@pytest.mark.django_db
@freezegun.freeze_time("2020-01-01 00:00:00", tick=False)
def test_api_workflow():
    """
    Test user, post and reaction creation using the api end points.
    """

    client = test.APIClient()

    # Create a user.
    data = {"username": "test user", "password": "pass1234"}
    create_user_response = client.post(urls.reverse("create-user"), data, fomat="json")
    assert create_user_response.status_code == status.HTTP_201_CREATED

    # Create a post.
    data = {
        "expires_at": f"{dt.now()}",
        "author": 1,
        "title": "My first post",
        "body": "A really long post body",
        "topics": ["Politics"],
    }
    create_post_response = client.post(
        urls.reverse("create-post"), data=data, format="json"
    )
    assert create_post_response.status_code == status.HTTP_201_CREATED

    # Add a reaction.
    first_reaction = {
        "like_or_dislike": "Like",
        "comment": "I really like this post",
        "author": 1,
        "post": 1,
    }
    add_reaction_response = client.post(
        urls.reverse("add-reaction"), data=first_reaction, format="json"
    )
    assert add_reaction_response.status_code == status.HTTP_201_CREATED

    # Get the post detail to check for successful creation of the post and reaction.
    post_detail_response = client.get("/posts/1", fomat="json")
    assert post_detail_response.status_code == status.HTTP_200_OK
    content = io.BytesIO(post_detail_response.content)
    data = parsers.JSONParser().parse(content)
    assert data == {
        "created_at": "2020-01-01T00:00:00Z",
        "expires_at": "2020-01-01T00:00:00Z",
        "author": 1,
        "reactions": ["2020-01-01 - test user - Like - I really like this post"],
        "title": "My first post",
        "body": "A really long post body",
        "topics": ["Politics"],
    }
