import factory

from ..models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'Username{}'.format(n))
    email = factory.Sequence(lambda n: 'email{}@email.com'.format(n))
