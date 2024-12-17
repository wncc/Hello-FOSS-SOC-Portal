from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
logger = logging.getLogger(__name__)

import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)

class CookieJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    def authenticate(self, request):
        logger.debug("Starting authentication process")
        
        # Check for JWT in cookies
        token = request.COOKIES.get('jwt')
        logger.debug(f"Token from cookies: {token}")
        
        # If not found in cookies, check the Authorization header
        if not token:
            auth_header = request.headers.get('Authorization')
            logger.debug(f"Authorization header: {auth_header}")
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                logger.debug(f"Token from Authorization header: {token}")

        if not token:
            logger.debug("No token found")
            return None

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            logger.debug(f"Payload: {payload}")
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            raise AuthenticationFailed('Invalid token')

        try:
            user = self.user_model.objects.get(id=payload['user_id'])
            logger.debug(f"Authenticated user: {user}")
        except self.user_model.DoesNotExist:
            logger.error("User not found")
            raise AuthenticationFailed('User not found')

        return (user, None)