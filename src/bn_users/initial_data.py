from django.utils.crypto import get_random_string

from bn_accounts.models import Account, Transaction
from .models import User


def load_data():
    load_users()


def load_users():
    inns = [
        '7714698320',
        '7715805253',
        '5036032527'
    ]

    for inn in inns:
        if not User.objects.filter(inn=inn).exists():
            password = get_random_string()
            user = User.objects.create_user(
                inn=inn,
                username='user{}'.format(inn),
                email='user{}@example.com'.format(inn),
                password=password,
            )
            print('email: {}, username: {}, password: {}'.format(user.email, user.username, password))

            account = Account.objects.create_for_user(user)
            Transaction.objects.create(account=account, amount=999)
            account.update_total()
