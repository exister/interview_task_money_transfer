from django.conf.urls import url

from .views import MoneyTransferView

urlpatterns = [
    url(r'^$', MoneyTransferView.as_view())
]
