from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
logger = logging.getLogger(__name__)


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = None
        try:
            header = super().authenticate(request)
        except Exception as e:
            logger.debug(f"Header login failed: {e}")

        
        if header is None:
            # Attempt to get token from the cookie
            token = request.COOKIES.get("auth")
            if token:
                return self.get_user(self.get_validated_token(token)), None

        return header, None
