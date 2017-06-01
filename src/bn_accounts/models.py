from itertools import chain

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models, transaction

from bn_core.models import TimeStampedModel


class MoneyTransferError(Exception):
    pass


class InsufficientFundsError(MoneyTransferError):
    pass


class AccountManager(models.Manager):
    def create_for_user(self, user):
        return self.get_or_create(user=user)[0]


class Account(TimeStampedModel, models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='account', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    objects = AccountManager()

    def transfer_money(self, accounts, amount):
        if self.total < amount:
            raise InsufficientFundsError

        with transaction.atomic():
            money_transfer = MoneyTransfer.objects.create(account_from=self, amount=amount)
            money_transfer.accounts_to.add(*accounts)

            per_account = amount / len(accounts)

            for account in accounts:
                Transaction.objects.create(
                    account=self,
                    corresponding_account=account,
                    description='Money transfer to account {}'.format(account.pk),
                    amount=-per_account
                )
                Transaction.objects.create(
                    account=account,
                    corresponding_account=self,
                    description='Money transfer from account {}'.format(self.pk),
                    amount=per_account
                )

            for account in chain(accounts, [self]):
                account.update_total()

            return money_transfer

    def update_total(self):
        self.total = self.transactions.all().aggregate(s=models.Sum('amount'))['s'] or 0
        self.save(update_fields=['total'])


class Transaction(TimeStampedModel, models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    corresponding_account = models.ForeignKey(
        Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='corresponding_transactions'
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=13, decimal_places=2)


class MoneyTransfer(TimeStampedModel, models.Model):
    account_from = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='outgoing_money_transfers')
    accounts_to = models.ManyToManyField(Account, related_name='incoming_money_transfers')
    amount = models.DecimalField(max_digits=13, decimal_places=2, validators=[MinValueValidator(0)])
