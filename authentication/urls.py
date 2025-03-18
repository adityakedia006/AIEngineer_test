from django.urls import path
from .views import register, login_user, get_user_details, logout_user, verify_otp, get_csrf_token

urlpatterns = [
    path("register/", register),
    path("register/verify/", verify_otp),
    path("login/", login_user),
    path("me/", get_user_details),
    path("logout/", logout_user),
    path("csrf-token/", get_csrf_token),
]