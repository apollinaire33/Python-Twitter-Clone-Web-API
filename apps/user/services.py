import datetime

import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed

from apps.user.models import User


class UserAuthentication:
    @staticmethod
    def generate_access_token(serializer):
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password for specified Email')

        payload = {
            'email': user.email,
            'exp': datetime.datetime.utcnow() + settings.PY_JWT['ACCESS_TOKEN_LIFETIME'],
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.PY_JWT['SIGNING_KEY'], algorithm=settings.PY_JWT['ALGORITHM'])

        return token
