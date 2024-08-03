from rest_framework import viewsets, permissions
from .models import Booking, Hotel, HotelOrder, RoomType
from .serializers import BookingSerializer, HotelSerializer, OrderSerializer, RoomTypeSerializer

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

# class RoomTypeViewSet(viewsets.ModelViewSet):
#     queryset = RoomType.objects.all()
#     serializer_class = RoomTypeSerializer

# class BookingViewSet(viewsets.ModelViewSet):
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff:
#             return Booking.objects.all()
#         elif user.is_authenticated:
#             return Booking.objects.filter(user=user)
#         else:
#             return Booking.objects.none()

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = HotelOrder.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff:
#             return HotelOrder.objects.all()
#         elif user.is_authenticated:
#             return HotelOrder.objects.filter(user=user)
#         else:
#             return HotelOrder.objects.none()
class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Allow read access to unauthenticated users

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