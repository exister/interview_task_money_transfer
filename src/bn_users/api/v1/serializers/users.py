from rest_framework import serializers

from ....validators import inn_validator, inn_exists
from ....models import User


class InnField(serializers.CharField):
    default_validators = [inn_validator, inn_exists]


class UserSerializer(serializers.ModelSerializer):
    inn = InnField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'inn')
