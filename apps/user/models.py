from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    avatar = models.CharField(max_length=200, default=settings.AWS_S3_BASE_USER_PROFILE_PHOTO)
    role = models.CharField(max_length=9, choices=Roles.choices, default=Roles.USER)

    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.role == self.Roles.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False

        return super().save(**kwargs)
