from rest_framework import serializers

from bn_users.api.v1.serializers.users import InnField
from ....models import Transaction, Account, MoneyTransfer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'user', 'total', 'updated_at')



class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    corresponding_account = AccountSerializer(required=False)

    class Meta:
        model = Transaction
        fields = ('id', 'account', 'corresponding_account', 'description', 'amount', 'created_at')


class MoneyTransferSerializer(serializers.ModelSerializer):
    inns_to = serializers.ListSerializer(child=InnField(), allow_empty=False, write_only=True)

    default_error_messages = {
        'insufficient_funds': 'Insufficient funds'
    }

    class Meta:
        model = MoneyTransfer
        fields = ('id', 'account_from', 'accounts_to', 'inns_to', 'amount')
        read_only_fields = ('accounts_to',)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs['account_from'].total < attrs['amount']:
            self.fail('insufficient_funds')

        attrs['accounts_to'] = list(Account.objects.filter(user__inn__in=attrs['inns_to']))
        return attrs

    def create(self, validated_data):
        account_from = validated_data['account_from']
        instance = account_from.transfer_money(validated_data['accounts_to'], validated_data['amount'])
        return instance