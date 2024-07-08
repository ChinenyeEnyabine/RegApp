from rest_framework import viewsets,permissions
from .models import Booking, Hotel, HotelOrder
from .serializers import HotelBookingSerializer, HotelSerializers, OrderSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializers

class HotelBookingViewSet(viewsets.ModelViewSet):
    # queryset = Booking.objects.all()
    serializer_class = HotelBookingSerializer
    def get_queryset(self):
        user=self.request.user
        if user.is_staff:
          return Booking.objects.all()
        elif user.is_authenticated:
           return Booking.objects.filter(user=user)
        else:
           return Booking.objects.none()
    # permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = HotelOrder.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return HotelOrder.objects.all()
        elif user.is_authenticated:
            return HotelOrder.objects.filter(user=user)
        else:
            return HotelOrder.objects.none()