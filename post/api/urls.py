from django.urls import path

from post.api.views import PostList, create_post

urlpatterns = [
    path("posts/", PostList.as_view(), name="posts"),
    path("posts/add", create_post, name="create-post"),
]
