from django.urls import include, path
from rest_framework import routers
from django.contrib import admin

from hotelbooking.views import BookingViewSet, HotelViewSet, OrderViewSet, RoomTypeViewSet

router = routers.DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'hotelbooking', BookingViewSet, basename='booking')
router.register(r'orders', OrderViewSet)
router.register(r'roomtypes', RoomTypeViewSet)

urlpatterns = [
    # Your other URL patterns
    path('hoteladmin/', admin.site.urls),
    path('api/', include(router.urls)),
]
