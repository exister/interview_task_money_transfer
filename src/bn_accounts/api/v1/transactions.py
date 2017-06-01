from django.db import transaction
from rest_framework.viewsets import ModelViewSet

from .serializers.transactions import MoneyTransferSerializer


class MoneyTransferViewSet(ModelViewSet):
    serializer_class = MoneyTransferSerializer

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            return super().create(request, *args, **kwargs)
