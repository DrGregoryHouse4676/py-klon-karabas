import django_filters as filters
from .models import Performance


class PerformanceFilter(filters.FilterSet):
    date_from = filters.IsoDateTimeFilter(field_name="show_time", lookup_expr="gte")
    date_to = filters.IsoDateTimeFilter(field_name="show_time", lookup_expr="lte")
    play = filters.CharFilter(field_name="play__title", lookup_expr="icontains")
    hall = filters.CharFilter(field_name="theatre_hall__name", lookup_expr="icontains")

    class Meta:
        model = Performance
        fields = ("date_from", "date_to", "play", "hall")
