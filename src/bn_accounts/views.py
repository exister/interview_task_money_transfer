from django.views.generic import TemplateView


class MoneyTransferView(TemplateView):
    template_name = 'bn_accounts/money_transfer.html'
