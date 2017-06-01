from django.conf import settings
from django.db import models

from bn_core.models import TimeStampedModel


class Account(TimeStampedModel, models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='account', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=13, decimal_places=2, default=0)


class Transaction(TimeStampedModel, models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    corresponding_account = models.ForeignKey(
        Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='corresponding_transactions'
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=13, decimal_places=2)
