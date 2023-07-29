import django_filters

from api.models import Transaction


class TransactionFilter(django_filters.FilterSet):

    class Meta:
        model = Transaction
        exclude = ('user',)
