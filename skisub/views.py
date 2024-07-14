# # views.py

# from rest_framework import status, viewsets, permissions
# from rest_framework.response import Response
# from .serializers import BillOperationSerializer, UtilityOrderSerializer
# from .models import BillOperation, UtilityOrder

# class BillOperationViewSet(viewsets.ModelViewSet):
#     queryset = BillOperation.objects.all()

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             data = self.request.data
#             if 'dataplan' in data:
#                 return BillOperationSerializer
#             elif 'rechargeplan' in data:
#                 return BillOperationSerializer
#             elif 'meterno' in data:
#                 return BillOperationSerializer
#             elif 'selectbouquet' in data:
#                 return BillOperationSerializer
#         return BillOperationSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         bill_operation = serializer.save()

#         order_data = {
#             'user': request.user.id,
#             'utility': bill_operation.id,
#             'total_amount': bill_operation.amount,
#             'status': 'pending'
#         }
#         order_serializer = UtilityOrderSerializer(data=order_data)
#         order_serializer.is_valid(raise_exception=True)
#         order_serializer.save()

#         headers = self.get_success_headers(serializer.data)
#         return Response(order_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# class UtilityOrderViewSet(viewsets.ModelViewSet):
#     queryset = UtilityOrder.objects.all()
#     serializer_class = UtilityOrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff:
#             return UtilityOrder.objects.all()
#         elif user.is_authenticated:
#             return UtilityOrder.objects.filter(user=user)
#         else:
#             return UtilityOrder.objects.none()
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import AirtimeTransactionSerializer, DataTransactionSerializer

class AirtimeTransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = AirtimeTransactionSerializer
    permission_classes = [IsAuthenticated]

class DataTransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = DataTransactionSerializer
    permission_classes = [IsAuthenticated]
