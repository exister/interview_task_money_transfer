from django.test import TestCase

from bn_accounts.models import Account, Transaction, InsufficientFundsError
from bn_users.tests.factories import UserFactory


class MoneyTransferTestCase(TestCase):
    def setUp(self):
        self.user1 = UserFactory.create(inn='7714698320')
        self.user2 = UserFactory.create(inn='7715805253')
        self.user3 = UserFactory.create(inn='5036032527')

        for user in (self.user1, self.user2, self.user3):
            account = Account.objects.create_for_user(user)
            Transaction.objects.create(account=account, amount=1000)
            account.update_total()

    def test_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.user1.account.transfer_money((self.user2.account, self.user3.account), 99999)

    def test_transfer_to_single_account(self):
        self.assertEqual(Account.objects.get(user=self.user1).total, 1000)
        self.assertEqual(Account.objects.get(user=self.user2).total, 1000)
        self.assertEqual(Account.objects.get(user=self.user3).total, 1000)

        self.user1.account.transfer_money((self.user2.account,), 100)

        self.assertEqual(Account.objects.get(user=self.user1).total, 900)
        self.assertEqual(Account.objects.get(user=self.user2).total, 1100)
        self.assertEqual(Account.objects.get(user=self.user3).total, 1000)

    def test_transfer_to_multiple_accounts(self):
        self.assertEqual(Account.objects.get(user=self.user1).total, 1000)
        self.assertEqual(Account.objects.get(user=self.user2).total, 1000)
        self.assertEqual(Account.objects.get(user=self.user3).total, 1000)

        self.user1.account.transfer_money((self.user2.account, self.user3.account), 100)

        self.assertEqual(Account.objects.get(user=self.user1).total, 900)
        self.assertEqual(Account.objects.get(user=self.user2).total, 1050)
        self.assertEqual(Account.objects.get(user=self.user3).total, 1050)
