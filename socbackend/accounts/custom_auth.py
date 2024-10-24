from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
logger = logging.getLogger(__name__)


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = None
        user = None
        try:
            user, token = super().authenticate(request)
            # print({user, token})
        except Exception as e:
            logger.debug(f"Header login failed: {e}")

        
        if token is None:
            # Attempt to get token from the cookie
            token = request.COOKIES.get("auth")
            if token:
                return self.get_user(self.get_validated_token(token)), None

        return user, token
