from rest_framework.test import APITestCase

from bn_accounts.models import Account, Transaction
from bn_users.tests.factories import UserFactory


class MoneyTransferTestCase(APITestCase):
    url = '/api/v1/accounts/money-transfer/'

    def setUp(self):
        self.user1 = UserFactory.create(inn='7714698320')
        self.user2 = UserFactory.create(inn='7715805253')
        self.user3 = UserFactory.create(inn='5036032527')

        for user in (self.user1, self.user2, self.user3):
            account = Account.objects.create_for_user(user)
            Transaction.objects.create(account=account, amount=1000)
            account.update_total()

    def test_validate_empty(self):
        response = self.client.post(
            self.url,
            data={},
        )
        self.assertEqual(response.status_code, 400)

    def test_validate_account_required(self):
        response = self.client.post(
            self.url,
            data={
                'inns_to': [
                    self.user2.inn,
                    self.user3.inn,
                ],
                'amount': 50
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('account_from', response.json())

    def test_validate_account_exists(self):
        response = self.client.post(
            self.url,
            data={
                'account_from': 0,
                'inns_to': [
                    self.user2.inn,
                    self.user3.inn,
                ],
                'amount': 50
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('account_from', response.json())

    def test_validate_inns_required(self):
        response = self.client.post(
            self.url,
            data={
                'account_from': self.user1.pk,
                'amount': 50
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('inns_to', response.json())

    def test_validate_inns_empty(self):
        response = self.client.post(
            self.url,
            data={
                'account_from': self.user1.pk,
                'inns_to': [],
                'amount': 50
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('inns_to', response.json())

    def test_validate_inn_invalid(self):
        response = self.client.post(
            self.url,
            data={
                'account_from': self.user1.pk,
                'inns_to': [
                    '1234567',
                ],
                'amount': 50
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('inns_to', response.json())

    def test_validate_inn_with_no_user(self):
        response = self.client.post(
            self.url,
            data={
                'account_from': self.user1.pk,
                'inns_to': [
                    '5032233705'
                ],
                'amount': 50
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('inns_to', response.json())

    def test_validate_amount_negative(self):
        response = self.client.post(
            self.url,
            data={
                'account_from': self.user1.pk,
                'inns_to': [
                    self.user2.inn,
                    self.user3.inn,
                ],
                'amount': -50
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('amount', response.json())

    def test_validate_amount_insufficient_funds(self):
        response = self.client.post(
            self.url,
            data={
                'account_from': self.user1.pk,
                'inns_to': [
                    self.user2.inn,
                    self.user3.inn,
                ],
                'amount': 999999
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.json())

    def test_money_transfer_single(self):
        self.assertEqual(Account.objects.get(user=self.user1).total, 1000)
        self.assertEqual(Account.objects.get(user=self.user2).total, 1000)
        self.assertEqual(Account.objects.get(user=self.user3).total, 1000)

        response = self.client.post(
            self.url,
            data={
                'account_from': self.user1.pk,
                'inns_to': [
                    self.user2.inn,
                ],
                'amount': 100
            },
        )
        self.assertEqual(response.status_code, 201)

        self.assertEqual(Account.objects.get(user=self.user1).total, 900)
        self.assertEqual(Account.objects.get(user=self.user2).total, 1100)
        self.assertEqual(Account.objects.get(user=self.user3).total, 1000)

    def test_money_transfer_multiple(self):
        self.assertEqual(Account.objects.get(user=self.user1).total, 1000)
        self.assertEqual(Account.objects.get(user=self.user2).total, 1000)
        self.assertEqual(Account.objects.get(user=self.user3).total, 1000)

        response = self.client.post(
            self.url,
            data={
                'account_from': self.user1.pk,
                'inns_to': [
                    self.user2.inn,
                    self.user3.inn,
                ],
                'amount': 100
            },
        )
        self.assertEqual(response.status_code, 201)

        self.assertEqual(Account.objects.get(user=self.user1).total, 900)
        self.assertEqual(Account.objects.get(user=self.user2).total, 1050)
        self.assertEqual(Account.objects.get(user=self.user3).total, 1050)
