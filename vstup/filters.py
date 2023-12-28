import django_filters
from .models import University, Entrant
from decimal import Decimal
from django.db.models import Q
import django_filters

class UniversityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Назва')
    shortName = django_filters.CharFilter(lookup_expr='icontains', label='Скорочення')
    location = django_filters.CharFilter(lookup_expr='icontains', label='Дислокація')

    class Meta:
        model = University
        fields = ['name', 'shortName', 'location']


class UniversityHTMXFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search', label="")

    class Meta:
        model = University
        fields = ['query']

    def universal_search(self, queryset, name, value):
        # Оскільки існує лише одна форма пошуку для всієї таблиці, я спочатку перевіряю,
        # чи є вхідні дані цифрами.
        # Якщо так, то шукаю тільки в стовпчиках price і cost.
        # В іншому випадку шукаю в стовпчиках name та category.

        # if value.replace(".", "", 1).isdigit():
        #     value = Decimal(value)
        #     return University.objects.filter(
        #         Q(price=value) | Q(cost=value)
        #     )

        return University.objects.filter(
            Q(name__icontains=value) | Q(shortName__icontains=value) | Q(location__icontains=value)
        )


# class EntrantsFilter(django_filters.FilterSet):
#     last_name = django_filters.CharFilter(lookup_expr='icontains', label="Прізвище")
#     specialty = django_filters.CharFilter(lookup_expr='icontains', label='Спеціальність')
#     department = django_filters.CharFilter(lookup_expr='icontains', label='Кафедра')
#
#     class Meta:
#         model = Entrant
#         fields = ['last_name', 'specialty', 'department']

class EntrantsFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(lookup_expr='icontains', label="Прізвище")
    specialty = django_filters.CharFilter(field_name='specialty__code', lookup_expr='icontains', label='Спеціальність')
    department = django_filters.CharFilter(field_name='department__shortName', lookup_expr='icontains', label='Кафедра')

    class Meta:
        model = Entrant
        fields = ['last_name', 'specialty', 'department']