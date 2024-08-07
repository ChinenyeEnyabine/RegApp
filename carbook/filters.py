from django_filters import rest_framework as filters
from .models import Car

class CarFilter(filters.FilterSet):
    price_per_day = filters.RangeFilter()
    
    class Meta:
        model = Car
        fields = {
            'model': ['exact'],
            'price_per_day': ['exact', 'lte', 'gte'],
            'transmission': ['exact'],
            'fuel_type': ['exact'],
            'year': ['exact', 'lte', 'gte'],
            'number_of_passengers': ['exact', 'lte', 'gte'],
            'number_of_doors': ['exact', 'lte', 'gte'],
            'max_power_hp': ['exact', 'lte', 'gte'],
            'top_speed_mph': ['exact', 'lte', 'gte'],
            'air_conditioning': ['exact'],
        }
