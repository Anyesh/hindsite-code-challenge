from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from account.api.serializers import ProfileSerializer, UserRegisterSerializer
from account.models import User
from hindsite.utils import get_response
from post.models import Post


class Ping(APIView):
    @method_decorator(cache_page(settings.CACHE_TTL))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request):

        serializer = ProfileSerializer(request.user.profile)

        return Response(
            data=get_response(
                message="Ping was a success!",
                result={"data": serializer.data},
                status=True,
                status_code=200,
            ),
            status=status.HTTP_200_OK,
        )


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer


class LogoutView(APIView):
    def logout(self, request):
        response = Response(
            data=get_response(message="User logged out", status=True, result="Success"),
            status=status.HTTP_200_OK,
        )

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except (TokenError, KeyError) as e:
            return Response(
                data=get_response(
                    message=f"Invalid token! {e}", status=False, result="Error"
                ),
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        django_logout(request)

        return response

    def post(self, request):
        return self.logout(request)


@api_view(["POST"])
def leave_organization(request):
    if not request.user.organization_id:
        return Response({"msg": "join the organization first"}, 401)
    user = User.objects.get(id=request.user.id)
    user.organization_id = None
    Post.objects.filter(user_id=user, organization_id=user.organization_id).update(
        is_deleted=True
    )
    user.save()
    return Response({"msg": "organization left!"}, 200)


@api_view(["POST"])
def join_organization(request):
    if request.user.organization_id:
        return Response({"msg": "You are already in an organization"}, 401)
    user = User.objects.get(id=request.user.id)
    user.organization_id = request.data.get("organization_id")
    user.save()
    return Response({"msg": "organization Joined!"}, 200)
