from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # User views.
    path("create-user/", views.CreateUserView.as_view(), name="create-user"),
    path("users/", views.UsersView.as_view(), name="users"),
    path("users/<int:pk>", views.DetailUserView.as_view(), name="detail-user"),
    # Post views.
    path("create-post", views.CreatePostView.as_view(), name="create-post"),
    path("posts", views.PostsView.as_view(), name="posts"),
    path("posts/<int:pk>", views.DetailPostView.as_view(), name="post-detail"),
    # Reaction views.
    path("add-reacion/", views.AddReactionView.as_view(), name="add-reaction"),
]


urlpatterns = format_suffix_patterns(urlpatterns)
