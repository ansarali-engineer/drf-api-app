from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
    get_md5_hash_password,
)
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings

from .models import User, UserToken


class CustomTokenAuthentication(BaseAuthentication):
    keyword = b'token'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword:
            return None
        if len(auth) != 2:
            raise AuthenticationFailed('Invalid token header.')

        try:
            key = auth[1].decode()
        except UnicodeError as exc:
            raise AuthenticationFailed('Invalid token.') from exc

        try:
            token = UserToken.objects.select_related('user').get(key=key)
        except UserToken.DoesNotExist as exc:
            raise AuthenticationFailed('Invalid token.') from exc

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        return token.user, token

    def authenticate_header(self, request):
        return 'Token'


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError as exc:
            raise InvalidToken(
                'Token contained no recognizable user identification.'
            ) from exc

        try:
            user = User.objects.get(
                **{api_settings.USER_ID_FIELD: user_id}
            )
        except User.DoesNotExist as exc:
            raise AuthenticationFailed(
                'User not found.',
                code='user_not_found',
            ) from exc

        if api_settings.CHECK_USER_IS_ACTIVE and not user.is_active:
            raise AuthenticationFailed(
                'User is inactive.',
                code='user_inactive',
            )

        if api_settings.CHECK_REVOKE_TOKEN:
            if validated_token.get(
                api_settings.REVOKE_TOKEN_CLAIM
            ) != get_md5_hash_password(user.password):
                raise AuthenticationFailed(
                    "The user's password has been changed.",
                    code='password_changed',
                )

        return user
