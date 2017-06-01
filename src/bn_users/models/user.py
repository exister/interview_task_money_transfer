from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models

from bn_core.models import TimeStampedModel

from .fields import INNField


class UserManager(BaseUserManager):
    pass


class User(TimeStampedModel, AbstractUser):
    inn = INNField(db_index=True)

    objects = UserManager()
