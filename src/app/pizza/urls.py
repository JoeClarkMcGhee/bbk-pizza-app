from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("oAuth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("", include("src.app.interfaces.api.urls")),
]
