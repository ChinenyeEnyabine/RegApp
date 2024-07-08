from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Car, Booking, CarImage, CarMake, CarModel
from .serializers import CarBookingSerializer, CarImageSerializer, CarSerializer, CarMakeSerializer, CarModelSerializer
class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer

class CarMakeViewSet(viewsets.ModelViewSet):
    queryset = CarMake.objects.all()
    serializer_class = CarMakeSerializer

class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CarBookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = CarBookingSerializer
    

    def get_queryset(self):
        user=self.request.user
        if user.is_staff:
            return Booking.objects.all()
        elif user.is_authenticated:
            return Booking.objects.filter(user=user)
        else:
            return Booking.objects.none()
    permission_classes=[permissions.IsAuthenticated]

from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        elif user.is_authenticated:
            return Order.objects.filter(user=user)
        else:
            return Order.objects.none()




