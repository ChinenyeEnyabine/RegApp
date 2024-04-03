import uuid
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
        
# from rest_framework import viewsets
# from rest_framework.response import Response
# from django.http import JsonResponse
# from .models import Transaction

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
#         # For the sake of demonstration, let's assume the expected signature is "expected_signature"
#         expected_signature = "BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7"
#         if x_auth_signature != expected_signature:
#             return JsonResponse({
#                 "requestSuccessful": False,
#                 "responseMessage": "Rejected transaction: Incorrect X-auth-Signature",
#                 "responseCode": "02"
#             })

#         # Check if the settlementId is already processed
#         if Transaction.objects.filter(settlementId=settlementId).exists():
#             return JsonResponse({
#                 "requestSuccessful": False,
#                 "responseMessage": "Duplicate transaction",
#                 "responseCode": "01"
#             })

#         # Assuming all other validations pass, return success response
      
#         return JsonResponse({
#             "requestSuccessful": True,
#             "sessionId": str(uuid.uuid4()),  # Generate a UUID for sessionId
#             "responseMessage": "Success",
#             "responseCode": "00"
#         })
        
# from rest_framework import viewsets
# from rest_framework.response import Response
# from django.http import JsonResponse
# from .models import Transaction

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

#         # Check if the settlementId is already processed
#         if self.is_duplicate_settlement_id(settlementId):
#             return JsonResponse({
#                 "requestSuccessful": False,
#                 "responseMessage": "Duplicate transaction",
#                 "responseCode": "01"
#             })

#         # Assuming all other validations pass, return success response
#         # Add settlementId to the processed_settlement_ids set
#         self.add_processed_settlement_id(settlementId)
        
#         return JsonResponse({
#             "requestSuccessful": True,
#             "sessionId": str(uuid.uuid4()),  # Generate a UUID for sessionId
#             "responseMessage": "Success",
#             "responseCode": "00"
#         })

#     def is_duplicate_settlement_id(self, settlementId):
#         # Check if settlementId already exists in the Transaction model
#         return Transaction.objects.filter(settlementId=settlementId).exists()

#     def add_processed_settlement_id(self, settlementId):
#         # Add new settlementId to the Transaction model
#         transaction = Transaction(settlementId=settlementId)
#         transaction.save()
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Transaction
import uuid  # for generating UUID

class TransactionView(viewsets.ViewSet):
    def create(self, request):
        # Extracting data from the request
        request_data = request.data
        sessionId = request_data.get("sessionId")
        settlementId = request_data.get("settlementId")
        virtualAccount = request_data.get("accountNumber")
        x_auth_signature = request.headers.get("X-auth-Signature")
        
        # Check if all required data is present
        if not all([sessionId, settlementId, virtualAccount, x_auth_signature]):
            return JsonResponse({
                "requestSuccessful": False,
                "responseMessage": "Rejected transaction: Missing required data",
                "responseCode": "02"
            })

        # Check if the X-auth-Signature matches the expected value
        expected_signature = "BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7"
        if x_auth_signature != expected_signature:
            return JsonResponse({
                "requestSuccessful": False,
                "responseMessage": "Rejected transaction: Incorrect X-auth-Signature",
                "responseCode": "02"
            })

        # Check if the settlementId is already processed
        if self.is_duplicate_settlement_id(settlementId):
            return JsonResponse({
                "requestSuccessful": False,
                "responseMessage": "Duplicate transaction",
                "responseCode": "01"
            })

        # Assuming all validations pass, create the transaction and return success response
        self.create_transaction(settlementId)
        
        return JsonResponse({
            "requestSuccessful": True,
            "sessionId": str(uuid.uuid4()),  # Generate a UUID for sessionId
            "responseMessage": "Success",
            "responseCode": "00"
        })

    def is_duplicate_settlement_id(self, settlementId):
        # Check if settlementId already exists in the Transaction model
        return Transaction.objects.filter(settlementId=settlementId).exists()

    def create_transaction(self, settlementId):
        # Create a new transaction with the given settlementId
        Transaction.objects.create(settlementId=settlementId)
