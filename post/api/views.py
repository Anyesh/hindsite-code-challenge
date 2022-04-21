from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from organization.models import Organization
from post.api.serializers import PostSerializer
from post.models import Post


class PostList(generics.ListAPIView):

    permission_classes = (AllowAny,)
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Post.objects.filter(
            organization_id=user.organization_id, is_deleted=False
        )


@api_view(["POST"])
def create_post(request):
    data = request.data.get("description")
    if not data:
        return Response({"msg": "Description field is required"}, status=401)

    organization = Organization.objects.filter(id=request.user.organization_id).first()
    if not organization:
        return Response({"msg": "Join the organization first"}, status=401)

    post = Post.objects.create(
        user_id=request.user,
        organization_id=organization,
        description=data,
    )
    post.save()
    return Response({"msg": "Post created succesfully!"}, status=201)
