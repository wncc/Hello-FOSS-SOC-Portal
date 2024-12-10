from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger(__name__)

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Attempt header authentication first
        header = None
        try:
            header = super().authenticate(request)
        except Exception as e:
            logger.debug(f"Header authentication failed: {e}")

        # Fallback to cookie-based authentication
        if header is None:
            token = request.COOKIES.get("auth")  # Fetch JWT from cookies
            if token:
                try:
                    validated_token = self.get_validated_token(token)
                    return self.get_user(validated_token), None
                except Exception as e:
                    logger.error(f"Cookie token validation failed: {e}")
                    return None

        return header

