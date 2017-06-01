import factory

from bn_users.tests.factories import UserFactory
from ..models import Account


class AccountFactory(factory.DjangoModelFactory):
    class Meta:
        model = Account

    user = factory.SubFactory(UserFactory)
