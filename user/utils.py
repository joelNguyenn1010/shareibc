from django.conf import settings
from django.utils import timezone
import datetime

# JWT_REFRESH_EXPIRATION_DELTA
expire_delta = settings.JWT_AUTH['JWT_EXPIRATION_DELTA']

def jwt_response_payload_handler(token, user=None, request=None):
    print(user)
    return {
        'token': token,
        'email': user.email,
        'name': user.first_name + " " + user.last_name,
        'expires_in': timezone.now() + expire_delta - datetime.timedelta(seconds=200)
    }
