from django.contrib.auth.models import AbstractUser
from django.db import models

from bn_core.models import TimeStampedModel

from .fields import INNField


class User(TimeStampedModel, AbstractUser):
    inn = INNField(db_index=True)
