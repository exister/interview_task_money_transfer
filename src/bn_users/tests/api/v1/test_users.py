from rest_framework.test import APITestCase

from bn_accounts.models import Account, Transaction
from bn_users.tests.factories import UserFactory


class MoneyTransferTestCase(APITestCase):
    url = '/api/v1/users/'

    def setUp(self):
        self.user1 = UserFactory.create(inn='7714698320')
        self.user2 = UserFactory.create(inn='7715805253')
        self.user3 = UserFactory.create(inn='5036032527')

        for user in (self.user1, self.user2, self.user3):
            account = Account.objects.create_for_user(user)
            Transaction.objects.create(account=account, amount=1000)
            account.update_total()

    def test_users_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.user1.pk,
                    "first_name": self.user1.first_name,
                    "last_name": self.user1.last_name,
                    "inn": self.user1.inn
                },
                {
                    "id": self.user2.pk,
                    "first_name": self.user2.first_name,
                    "last_name": self.user2.last_name,
                    "inn": self.user2.inn
                },
                {
                    "id": self.user3.pk,
                    "first_name": self.user3.first_name,
                    "last_name": self.user3.last_name,
                    "inn": self.user3.inn
                }
            ]
        })

    def test_users_search(self):
        response = self.client.get(self.url, data={'search': self.user1.inn})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.user1.pk,
                    "first_name": self.user1.first_name,
                    "last_name": self.user1.last_name,
                    "inn": self.user1.inn
                }
            ]
        })
