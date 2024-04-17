from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, APIException

from datetime import timedelta
from django.utils import timezone
from django.conf import settings


class ExtendToken(APIException):
    status_code = 401
    default_detail = 'Token extended'
    default_code = '401'

#this return left time
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    token_expired_after_seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS

    # if token.user.roleuser_user.role_id in [1,2,3]:
    #     token_expired_after_seconds = 21600 # 6 hours

    left_time = timedelta(seconds = token_expired_after_seconds) - time_elapsed
    return left_time

#this return left time
def recreated_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_RECREATED_AFTER_SECONDS) - time_elapsed
    return left_time

# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)

# token checker if token expired or not
def recreate_token(token):
    return recreated_in(token) < timedelta(seconds = 0)

# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    can_recreate_token = recreate_token(token)
    
    # # recreate_token = False

    # if is_expired:
    #     token = Token.objects.get(user = token.user)
    #     token.delete()
    # elif (can_recreate_token and not is_expired):
    #     token = Token.objects.get(user = token.user)
    #     user = token.user
    #     token.delete()
    #     token = Token.objects.create(user=user)

    return is_expired, token, can_recreate_token

    # is_expired = is_token_expired(token)
    # is_recreated = False
    # if is_expired:
    #     print(">>>>>>>expire")
    #     print(token)
    #     user = token.user
    #     # token.delete()
    #     token = Token.objects.get(user = token.user)
    #     token.delete()

    #     token = Token.objects.create(user=user)
    #     print("<<<<<<<<<<<new token create" + token.key)
    #     is_recreated = True


    # return is_expired, token, can_recreate_token

# def token_expire_handler(token):
#     is_expired = is_token_expired(token)
#     if is_expired:


#         EXTENDED_SESSION_DAYS = 60
#         EXPIRE_THRESHOLD = 30

#         # if request.user.is_authenticated():
#         now = timezone.now()

#             # Only extend the session if the current expiry_date is less than 30 days from now
#         if expires_in(token) < now + timedelta(days=EXPIRE_THRESHOLD):
#             request.session.set_expiry(now + timedelta(days=EXTENDED_SESSION_DAYS))

#         token.delete()
#         token = Token.objects.create(user = token.user)
#     return is_expired, token


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    If token is expired then it will be removed
    and new one with different key will be created
    """
    def authenticate(self, request):
        # return super().authenticate(request)
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token, request)

    def authenticate_credentials(self, key, request):
        try:
            token = Token.objects.get(key = key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")
        
        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")

        # from detectone import custom_exception_handler

        picky_url = ['/notifications/staff/', '/notifications/client/']

        if request.get_full_path() not in picky_url:
            is_expired, token, can_generate_token = token_expire_handler(token)

            if (can_generate_token and not is_expired):
                token = Token.objects.get(user = token.user)
                user = token.user
                token.delete()
                token = Token.objects.create(user=user)
                print(token.key)
                raise ExtendToken("regenerate " + token.key, token)
            elif is_expired:
                print(token.key)
                token = Token.objects.get(user = token.user)
                token.delete()
                raise AuthenticationFailed("The Token is expired")
        # else:
        #     token = Token.objects.get(user = token.user)
        #     print(is_expired)
        #     print(can_generate_token)
        #     user = token.user
        #     token.delete()
        #     raise AuthenticationFailed("The Token is expired")

        return (token.user, token)