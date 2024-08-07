
from rest_framework import serializers

from account.serializers import TransactionSerializer
from carbook.serializers import  CarOrderList
from hotelbooking.serializers import HotelOrderSerializer
class CombinedOrderSerializer(serializers.Serializer):
    transactions = TransactionSerializer(many=True)
    hotel_orders = HotelOrderSerializer(many=True)
    car_orders = CarOrderList(many=True)