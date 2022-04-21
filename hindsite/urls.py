from typing import List

from django.contrib import admin
from django.urls import include, path
from django.urls.resolvers import URLResolver

api_urls: List[URLResolver] = [
    path("", include("account.api.urls")),
    path("", include("organization.api.urls")),
    path("", include("post.api.urls")),
]


urlpatterns: List[URLResolver] = [
    path("", include("main.urls")),
    path("api/", include(api_urls)),
    path("admin/", admin.site.urls),
]
