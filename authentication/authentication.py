from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()

class CookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_token = request.COOKIES.get("auth_token")
        if not auth_token:
            return None
        try:
            user = User.objects.get(id=auth_token)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid authentication token.")
        return (user, None)
