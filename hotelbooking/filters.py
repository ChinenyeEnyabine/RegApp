
from django_filters import rest_framework as filters
from .models import RoomType

class RoomTypeFilter(filters.FilterSet):
    price_per_day = filters.RangeFilter()  # Range filter for price per day
    hotel = filters.CharFilter(field_name='hotel__name', lookup_expr='icontains')  # Filter by hotel name
    available = filters.BooleanFilter()  # Filter by availability

    class Meta:
        model = RoomType
        fields = {
            'price_per_day': ['exact', 'lte', 'gte'],
            'hotel': ['exact'],  # You can add more lookup types as needed
            'available': ['exact'],
            'name': ['exact', 'icontains'],  # Filter by room type name
        }
