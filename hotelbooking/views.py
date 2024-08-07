from rest_framework import viewsets, permissions, filters

from hotelbooking.filters import RoomTypeFilter
from .models import Booking, Hotel, HotelOrder, RoomType
from .serializers import BookingSerializer, HotelOrderSerializer, HotelSerializer, OrderSerializer, RoomTypeSerializer
from django_filters.rest_framework import DjangoFilterBackend

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location', 'amenities']
    search_fields = ['name']
    
class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Allow read access to unauthenticated users
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RoomTypeFilter  # Use the custom filter class
    search_fields = ['name', 'hotel__name']  # Allow search by room type name and hotel name

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        elif user.is_authenticated:
            return Booking.objects.filter(user=user)
        else:
            return Booking.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Check if the user is authenticated
        if user.is_staff:
            return HotelOrder.objects.all()
        elif user.is_authenticated:
            return HotelOrder.objects.filter(user=user)
        else:
            return HotelOrder.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HotelOrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotelOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Check if the user is authenticated
        if user.is_staff:
            return HotelOrder.objects.all()
        elif user.is_authenticated:
            return HotelOrder.objects.filter(user=user)
        else:
            return HotelOrder.objects.none()