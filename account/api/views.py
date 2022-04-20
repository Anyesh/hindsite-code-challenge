import json

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

from account.api.serializers import (
    ProfileSerializer,
    UserRegisterSerializer,
    UserSerializer,
)
from account.models import User
from helpers.api_error_response import error_response
from helpers.error_messages import INVALID_REQUEST
from hindsite.utils import get_response


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


def token_response(token):
    return json.loads('{"token": "' + str(token) + '"}')


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer


@api_view(["PUT"])
def edit_profile(request):

    try:
        user_object = User.objects.get(id=request.user.id)
        user_object.first_name = request.data["first_name"]
        user_object.last_name = request.data["last_name"]
        user_object.save()

        return Response(
            data={
                **token_response(request.headers["Authorization"].split()[-1]),
                **UserSerializer(user_object).data,
            },
            status=status.HTTP_200_OK,
        )
    except User.DoesNotExist:
        return Response(
            data=error_response(INVALID_REQUEST), status=status.HTTP_400_BAD_REQUEST
        )


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
        response.delete_cookie(settings.JWT_AUTH_COOKIE)
        response.delete_cookie(settings.JWT_AUTH_REFRESH_COOKIE)
        return response

    def post(self, request):
        return self.logout(request)
