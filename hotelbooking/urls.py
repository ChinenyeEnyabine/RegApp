from django.urls import include, path
from rest_framework import routers
from django.contrib import admin

from hotelbooking.views import HotelBookingViewSet, HotelViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'hotelbooking', HotelBookingViewSet,basename='booking')
router.register(r'orders', OrderViewSet)
urlpatterns = [
    # Your other URL patterns
    path('hoteladmin/',admin.site.urls),
    path('api/', include(router.urls)),
]
