from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account.api.views import (
    LogoutView,
    Ping,
    Register,
    join_organization,
    leave_organization,
)

urlpatterns = [
    path("user/ping/", Ping.as_view(), name="ping"),
    path("user/join-organization", join_organization, name="join_organization"),
    path("user/leave-organization", leave_organization, name="leave_organization"),
    path("auth/login", TokenObtainPairView.as_view(), name="login"),
    path("auth/register", Register.as_view(), name="register"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    path("auth/token/refresh", TokenRefreshView().as_view(), name="token_refresh"),
]
