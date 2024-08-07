from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from carbook.models import Order
from hotelbooking.models import HotelOrder
from .models import Transaction
from .combined_serializer import CombinedOrderSerializer

class CombinedOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        # Get the authenticated user
        user = request.user

        # Fetch Transactions related to the user using their account_number
        transactions = Transaction.objects.filter(accountNumber=user.account_number)

        # Fetch Hotel Orders related to the user
        hotel_orders = HotelOrder.objects.filter(user=user)

        # Fetch Car Orders related to the user
        car_orders = Order.objects.filter(user=user)

        # Serialize combined data
        serializer = CombinedOrderSerializer({
            'transactions': transactions,
            'hotel_orders': hotel_orders,
            'car_orders': car_orders
        })

        return Response(serializer.data)
