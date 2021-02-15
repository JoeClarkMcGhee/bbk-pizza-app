from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # User views.
    path("create-user/", views.CreateUserView.as_view()),
    path("users/", views.UsersView.as_view()),
    path("users/<int:pk>", views.DetailUserView.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
