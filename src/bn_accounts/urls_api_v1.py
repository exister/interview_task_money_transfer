from django.conf.urls import url

from .api.v1.transactions import MoneyTransferViewSet


urlpatterns = [
    url('^accounts/money-transfer/$', MoneyTransferViewSet.as_view({'post': 'create'}), name='money-transfer-list'),
]
