import django_filters
from .models import *


class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.IsoDateTimeFilter(
        field_name='created_at', lookup_expr='exact')

    class Meta:
        model = Order
        fields = {
            'created_at': ['exact'],
            'user__username': ['icontains'],
        }


class TransactionsFilter(django_filters.FilterSet):
    created_at = django_filters.IsoDateTimeFilter(
        field_name='created_at', lookup_expr='exact')

    class Meta:
        model = Payment
        fields = {
            'created_at': ['exact'],
            'user__username': ['icontains'],
            'amount': ['icontains'],
            'fee_type__name': ['icontains'],
        }
