
from rest_framework import viewsets
from .models import Booking, Flight
from .serializers import BookingSerializer,AdminFlightSerializer, ListBookingSerializer
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class ListBookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = ListBookingSerializer
    
class AdminFlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = AdminFlightSerializer


