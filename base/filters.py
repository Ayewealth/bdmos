import django_filters
from .models import *


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'created_at': ['exact', 'year__gt', 'month__gt', 'day__gt'],
            'user__username': ['icontains'],
        }
