from django.urls import include, path
from rest_framework import routers
from django.contrib import admin

from hotelbooking.views import BookingViewSet, HotelOrderViewSet, HotelViewSet, OrderViewSet, RoomTypeViewSet

router = routers.DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'hotelbooking', BookingViewSet, basename='booking')
router.register(r'orders', OrderViewSet, basename='Hotelorder')
router.register(r'roomtypes', RoomTypeViewSet, basename='Roomtype')
router.register(r'listofhotelorder', HotelOrderViewSet, basename='orderlist')


urlpatterns = [
    # Your other URL patterns
    path('hoteladmin/', admin.site.urls),
    path('api/', include(router.urls)),
]
