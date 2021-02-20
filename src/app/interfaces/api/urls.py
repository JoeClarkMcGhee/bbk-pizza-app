from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from src.app.interfaces.api.views import post_views, reaction_views, user_views

urlpatterns = [
    # User views.
    path("create-user/", user_views.CreateUserView.as_view(), name="create-user",),
    path("users/", user_views.UsersView.as_view(), name="users",),
    path("users/<int:pk>", user_views.DetailUserView.as_view(), name="detail-user",),
    path(
        "users/<str:username>",
        user_views.DetailUserViewByName.as_view(),
        name="detail-user-by-name",
    ),
    # Post views.
    path("create-post", post_views.CreatePostView.as_view(), name="create-post",),
    path("posts", post_views.PostsView.as_view(), name="posts",),
    path("posts/<int:pk>", post_views.DetailPostView.as_view(), name="post-detail",),
    # Reaction views.
    path(
        "add-reacion/", reaction_views.AddReactionView.as_view(), name="add-reaction",
    ),
]


urlpatterns = format_suffix_patterns(urlpatterns)
