from django.shortcuts import render
from rest_framework.views import APIView
from knox.models import AuthToken
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import  login
from rest_framework.response import Response

from account.models import User, Transaction
from rest_framework import status, viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from account.serializers import LoginSerializer, RegisterSerializer, TransactionSerializer
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        form = AuthenticationForm(data=request.data)
        if form.is_valid():
            user = form.get_user()
            login(request, user=form.get_user())

            
            response = {
                "status_code": status.HTTP_200_OK,
                "success": "true",
                "message": "Successfully logged in",
                "data": LoginSerializer(user).data,
                "token": AuthToken.objects.create(user)[1]
            }
            return Response(response)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


    
# class TransactionView(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
        
from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.response import Response

# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

#     def perform_create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         # Perform custom logic to check settlement ID
#         settlement_id = request.data.get('settlementId')
#         print(settlement_id)
#         response_data = {}
        
#         # Check if the settlement ID already exists in the database
#         transactchek = Transaction.objects.filter(settlementId=settlement_id).exists()
#         print(transactchek)
#         if transactchek:

#             response_data = {
#                 "requestSuccessful": True,
#                 "sessionId": request.data.get("sessionId"),
#                 "responseMessage": "existing transaction",
#                 "responseCode": "01"
#             }
#         else:
#             # Perform additional checks here if needed
#             # For example, check if the settlement ID is in a certain range
#             # and consider it as a failure if it doesn't meet the criteria
            
#             # If the settlement ID doesn't exist, treat it as a success
#             response_data = {
#                 "requestSuccessful": True,
#                 "sessionId": request.data.get("sessionId"),
#                 "responseMessage": "success",
#                 "responseCode": "00"
#             }
        
#         return Response(response_data)
# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         # Perform custom logic to check settlement ID
#         settlement_id = request.data.get('settlementId')
#         print(settlement_id)
#         response_data = {}
        
#         # Check if the settlement ID already exists in the database
#         transact_check = Transaction.objects.filter(settlementId=settlement_id).exists()
#         print(transact_check)
#         if transact_check:
#             response_data = {
#                 "requestSuccessful": True,
#                 "sessionId": request.data.get("sessionId"),
#                 "responseMessage": "existing transaction",
#                 "responseCode": "01"
#             }
#         else:
#             # Create the transaction object
#             transaction_data = {
#                 'settlementId': settlement_id,
#                 # Add other fields as needed from the request data
#             }
#             # Assuming TransactionSerializer is used for creation as well
#             new_transaction_serializer = self.get_serializer(data=transaction_data)
#             new_transaction_serializer.is_valid(raise_exception=True)
#             new_transaction_serializer.save()  # Save the new transaction
#             response_data = {
#                 "requestSuccessful": True,
#                 "sessionId": request.data.get("sessionId"),
#                 "responseMessage": "success",
#                 "responseCode": "00"
#             }
        
#         return Response(response_data)

# from rest_framework import viewsets
# from rest_framework.response import Response
# from .models import Transaction
# from .serializers import TransactionSerializer

# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         # Perform custom logic to check settlement ID
#         settlement_id = request.data.get('settlementId')
        
#         # Check if the settlement ID already exists in the database
#         transact_check = Transaction.objects.filter(settlementId=settlement_id).exists()

#         if transact_check:
#             response_data = {
#                 "requestSuccessful": True,
#                 "sessionId": request.data.get("sessionId"),
#                 "responseMessage": "existing transaction",
#                 "responseCode": "01"
#             }
#         else:
#             # Create the transaction object only if the settlementId doesn't exist
#             serializer.save()
#             response_data = {
#                 "requestSuccessful": True,
#                 "sessionId": request.data.get("sessionId"),
#                 "responseMessage": "success",
#                 "responseCode": "00"
#             }
        
#         return Response(response_data)
# from rest_framework import viewsets
# from rest_framework.response import Response
# from .models import Transaction
# from .serializers import TransactionSerializer
# from rest_framework import status

# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         # Perform custom logic to check settlement ID
#         settlement_id = request.data.get('settlementId')
        
#         # Check if the settlement ID already exists in the database
#         transact_check = Transaction.objects.filter(settlementId=settlement_id).exists()

#         if transact_check:
#             response_data = {
#                 "requestSuccessful": True,
#                 "sessionId": request.data.get("sessionId"),
#                 "responseMessage": "existing transaction",
#                 "responseCode": "01"
#             }
#             return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             # Create the transaction object only if the settlementId doesn't exist
#             serializer.save()
#             response_data = {
#                 "requestSuccessful": True,
#                 "sessionId": request.data.get("sessionId"),
#                 "responseMessage": "success",
#                 "responseCode": "00"
#             }
#             return Response(response_data, status=status.HTTP_201_CREATED)
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Transaction

# class TransactionView(viewsets.ViewSet):

#     def create(self, request):
#         # Extracting data from the request body
#         request_data = request.data
#         sessionId = request_data.get("sessionId")
#         settlementId = request_data.get("settlementId")
#         virtualAccount = request_data.get("accountNumber")
#         x_auth_signature = request.headers.get("X-auth-Signature")
        
#         # Check if all required data is present
#         if not sessionId or not settlementId or not virtualAccount or not x_auth_signature:
#             # Return a rejected response if any required data is missing
#             return JsonResponse({
#                 "requestSuccessful": False,
#                 "responseMessage": "Rejected transaction: Missing required data",
#                 "responseCode": "02"
#             })

#         # Perform additional checks based on the provided requirements
        
#         # Check if the X-auth-Signature matches the expected value
#         expected_signature = "BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7"
#         if x_auth_signature != expected_signature:
#             return JsonResponse({
#                 "requestSuccessful": False,
#                 "responseMessage": "Rejected transaction: Incorrect X-auth-Signature",
#                 "responseCode": "02"
#             })

#         if Transaction.objects.filter(settlementId=settlementId).exists():
#             return JsonResponse({
#                 "requestSuccessful": False,
#                 "responseMessage": "Rejected transaction: duplicate settlement acount",
#                 "responseCode": "02"
#             })
#         else:
#             Transaction.objects.create()


# class TransactionViewSet(viewsets.ViewSet):
#     def create(self, request):
#         settlement_id = request.data.get('settlementId')
#         if Transaction.objects.filter(settlementId=settlement_id).exists():
#             return Response({'message': 'Existing settlement ID'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             # Assuming you have a serializer for creating Transaction objects
#             serializer = TransactionSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         settlement_id = serializer.validated_data.get('settlementId')
        
#         # Check if transaction with settlementId already exists
#         if Transaction.objects.filter(settlementId=settlement_id).exists():
#             return Response({"message": "Transaction with this settlementId already exists."}, status=400)

#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=201, headers=headers)
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    def create(self, request):
        # Extracting data from the request body
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_data = request.data
        sessionId = request_data.get("sessionId")
        settlementId = request_data.get("settlementId")
        virtualAccount = request_data.get("account_number")
        # headers = {'Content-Type': 'application/json', 'X-Auth-Signature': "BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7"}
        x_auth_signature = request.headers.get("X-Auth-Signature")
        # x_auth_signature = headers.get('X-Auth-Signature')
        # Check if all required data is present
        if not sessionId or not settlementId or not virtualAccount:
            # Return a rejected response if any required data is missing
            return JsonResponse({
                "requestSuccessful": False,
                "responseMessage": "Rejected transaction: Missing required data",
                "responseCode": "02"
            })

        # Perform additional checks based on the provided requirements
        
        # Check if the X-auth-Signature matches the expected value
        expected_signature = "BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7"
        if x_auth_signature != expected_signature:
            return JsonResponse({
                "requestSuccessful": False,
                "responseMessage": "Rejected transaction: Incorrect X-auth-Signature",
                "responseCode": "02"
            })

        if Transaction.objects.filter(settlementId=settlementId).exists():
            return JsonResponse({
                "requestSuccessful": False,
                "responseMessage": "Rejected transaction: duplicate settlement acount",
                "responseCode": "02"
            })
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
