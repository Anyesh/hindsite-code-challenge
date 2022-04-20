from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account.api.views import LogoutView, Ping, Register, edit_profile

urlpatterns = [
    path("user/ping/", Ping.as_view(), name="ping"),
    path("user/edit/", edit_profile),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/register/", Register.as_view(), name="register"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/token/refresh/", TokenRefreshView().as_view(), name="token_refresh"),
]
