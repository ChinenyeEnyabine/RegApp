from rest_framework.routers import DefaultRouter
from .views import TransactionalViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('transactionuser', TransactionalViewSet, basename='transaction')

urlpatterns = [
    path('tran/', include(router.urls)),
]
