from django.shortcuts import render
from rest_framework import viewsets, permissions, filters

from carbook.filters import CarFilter
from .models import Car, Booking, CarImage, CarMake, CarModel, Order
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    CarBookingSerializer, 
    CarImageSerializer,
    CarOrderList, 
    CarSerializer, 
    CarMakeSerializer, 
    CarModelSerializer,
    ListCarBookingSerializer,
    OrderSerializer
)

class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CarMakeViewSet(viewsets.ModelViewSet):
    queryset = CarMake.objects.all()
    serializer_class = CarMakeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['model', 'price_per_day']
    # search_fields = ['name']
    filterset_class = CarFilter
    search_fields = ['model__name', 'model__make__name']

    def get_queryset(self):
        return super().get_queryset().filter(available=True)

# class CarBookingViewSet(viewsets.ModelViewSet):
#     serializer_class = CarBookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff:
#             return Booking.objects.all()
#         elif user.is_authenticated:
#             return Booking.objects.filter(user=user)
#         else:
#             return Booking.objects.none()

#     def perform_create(self, serializer):
#         # Assign the user to the booking
#         serializer.save(user=self.request.user)

# class OrderViewSet(viewsets.ModelViewSet):
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff:
#             return Order.objects.all()
#         elif user.is_authenticated:
#             return Order.objects.filter(user=user)
#         else:
#             return Order.objects.none()

#     def perform_create(self, serializer):
#         # Assign the user to the order
#         serializer.save(user=self.request.user)

class CarBookingViewSet(viewsets.ModelViewSet):
    serializer_class = CarBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        elif user.is_authenticated:
            return Booking.objects.filter(user=user)
        return Booking.objects.none()

    def perform_create(self, serializer):
        # Assign the user to the booking
        serializer.save(user=self.request.user)
       
class ListCarBookingViewSet(viewsets.ModelViewSet):
    serializer_class = ListCarBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        elif user.is_authenticated:
            return Booking.objects.filter(user=user)
        return Booking.objects.none()

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        elif user.is_authenticated:
            return Order.objects.filter(user=user)
        return Order.objects.none()

    def perform_create(self, serializer):
        # Assign the user to the order
        serializer.save(user=self.request.user)
class OrderListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CarOrderList
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        elif user.is_authenticated:
            return Order.objects.filter(user=user)
        return Order.objects.none()