from .models import User
from django.db.models import F, Q
from django_filters import BaseInFilter, NumberFilter, CharFilter, rest_framework as filters



class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class CharInFilter(BaseInFilter, CharFilter):
    pass


class UsersFilter(filters.FilterSet):
    fulltext = filters.CharFilter(method='custom_filter', label="Search")

    class Meta:
        model = User
        fields = ['fulltext']

    def custom_filter(self, queryset, name, value):
        search_value = ' '.join(value.split()).split(' ')
        q_filter = Q()
        for item in search_value:
            # q_filter &= Q(email__icontains=item) | Q(first_name__icontains=item) | Q(last_name__icontains=item) | Q(username__icontains=item) | Q(role_name__icontains=item)
            q_filter &= Q(email__icontains=item) | Q(first_name__icontains=item) | Q(last_name__icontains=item) | Q(username__icontains=item)

        return queryset.filter(q_filter)
