import datetime
from pathlib import Path

import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from api.aws import S3
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


class Avatar:
    @staticmethod
    def validate_avatar_format(file):
        file_format = Path(file).suffix
        correct_formats = ['.jpg', '.jpeg', '.png']

        if file_format not in correct_formats:
            content = {'error': 'Wrong format of file for avatar'}
            raise ValidationError(content)

    @staticmethod
    def set_serializer_avatar(request, serializable_instance, obj):
        if request.method in ['GET', 'DELETE']:
            serializable_instance['avatar'] = S3().get_file(obj.avatar)
        elif request.method == 'PUT':
            serializable_instance['avatar'] = S3().get_presigned_url(obj.avatar)

        return serializable_instance

    def set_instance_avatar(self, request, image, instance, avatar_folder, base_photo):
        if request.method == 'PUT':
            self.validate_avatar_format(image)
            instance.avatar = f'{avatar_folder}{instance.id}-{image}'
        elif request.method == 'DELETE':
            S3().delete_file(instance.image)
            instance.image = base_photo

        instance.save()
        return instance
