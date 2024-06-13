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


from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Transaction



from rest_framework import viewsets
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer

# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     def create(self, request):
#         # Extracting data from the request body
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         request_data = request.data
#         sessionId = request_data.get("sessionId")
#         settlementId = request_data.get("settlementId")
#         virtualAccount = request_data.get("account_number")
#         # headers = {'Content-Type': 'application/json', 'X-Auth-Signature': "BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7"}
#         x_auth_signature = request.headers.get("X-Auth-Signature")
#         # x_auth_signature = headers.get('X-Auth-Signature')
#         # Check if all required data is present
#         if not sessionId or not settlementId or not virtualAccount:
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
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=201, headers=headers)

# from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from django.http import JsonResponse
# from account.models import Transaction
# from account.serializers import TransactionSerializer

# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         try:
#             # Extracting data from the request body
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             request_data = request.data

#             # Extracting required fields
#             sessionId = request_data.get("sessionId")
#             settlementId = request_data.get("settlementId")
#             virtualAccount = request.user.account_number  # Use the authenticated user's account number
#             x_auth_signature = request.headers.get("X-Auth-Signature")

#             # Expected X-auth-Signature
#             expected_signature = "BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7"

#             # Check for missing required data
#             if not sessionId or not settlementId or not virtualAccount:
#                 return JsonResponse({
#                     "requestSuccessful": True,
#                     "sessionId": "99990000554443332221",
#                     "responseMessage": "rejected transaction",
#                     "responseCode": "02"
#                 })

#             # Check if the X-auth-Signature matches the expected value
#             if x_auth_signature != expected_signature:
#                 return JsonResponse({
#                     "requestSuccessful": True,
#                     "sessionId": "99990000554443332221",
#                     "responseMessage": "rejected transaction",
#                     "responseCode": "02"
#                 })

#             # Check for duplicate settlementId
#             if Transaction.objects.filter(settlementId=settlementId).exists():
#                 return JsonResponse({
#                     "requestSuccessful": True,
#                     "sessionId": "99990000554443332221",
#                     "responseMessage": "duplicate transaction",
#                     "responseCode": "01"
#                 })

#             # Create the transaction
#             serializer.save(user=request.user, account_number=virtualAccount)
#             headers = self.get_success_headers(serializer.data)

#             return Response({
#                 "requestSuccessful": True,
#                 "sessionId": "99990000554443332221",
#                 "responseMessage": "success",
#                 "responseCode": "00"
#             }, status=status.HTTP_201_CREATED, headers=headers)

#         except Exception as e:
#             return JsonResponse({
#                 "requestSuccessful": True,
#                 "sessionId": "99990000554443332221",
#                 "responseMessage": "system failure, retry",
#                 "responseCode": "03"
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class UserTransactionViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = TransactionSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Transaction.objects.filter(user=user)


# class AdminTransactionViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     permission_classes = [IsAdminUser]

# views.py
# from rest_framework import viewsets, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from django.http import JsonResponse
# from account.models import Transaction
# from account.serializers import TransactionSerializer
# import logging

# logger = logging.getLogger(__name__)

# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     # permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         try:
#             # Log the request data and headers for debugging
#             logger.debug(f"Request data: {request.data}")
#             logger.debug(f"Request headers: {request.headers}")

#             # Extracting data from the request body
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             request_data = request.data

#             # Extracting required fields
#             sessionId = request.session.session_key  # Using the session key
#             settlementId = request_data.get("settlementId")
#             x_auth_signature = request.headers.get("X-Auth-Signature")
#             logger.debug(f"Session ID: {sessionId}")
#             logger.debug(f"Settlement ID: {settlementId}")
#             logger.debug(f"X-Auth-Signature: {x_auth_signature}")

#             # Expected X-auth-Signature
#             expected_signature = "BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7"

#             # Check for missing required data
#             if not sessionId or not settlementId:
#                 logger.warning("Missing required fields")
#                 return JsonResponse({
#                     "requestSuccessful": True,
#                     "sessionId": str(sessionId),
#                     "responseMessage": "rejected transaction",
#                     "responseCode": "02"
#                 })

#             # Check if the X-auth-Signature matches the expected value
#             if x_auth_signature != expected_signature:
#                 logger.warning("Invalid X-Auth-Signature")
#                 return JsonResponse({
#                     "requestSuccessful": True,
#                     "sessionId": str(sessionId),
#                     "responseMessage": "rejected transaction",
#                     "responseCode": "02"
#                 })

#             # Check for duplicate settlementId
#             if Transaction.objects.filter(settlementId=settlementId).exists():
#                 logger.warning("Duplicate settlementId")
#                 return JsonResponse({
#                     "requestSuccessful": True,
#                     "sessionId": str(sessionId),
#                     "responseMessage": "duplicate transaction",
#                     "responseCode": "01"
#                 })

#             # Create the transaction
#             transaction = serializer.save(user=request.user)
#             headers = self.get_success_headers(serializer.data)
#             logger.info("Transaction created successfully")

#             return Response({
#                 "requestSuccessful": True,
#                 "sessionId": str(sessionId),
#                 "responseMessage": "success",
#                 "responseCode": "00"
#             }, status=status.HTTP_201_CREATED, headers=headers)

#         except Exception as e:
#             logger.error(f"Exception in creating transaction: {str(e)}", exc_info=True)
#             return JsonResponse({
#                 "requestSuccessful": True,
#                 "sessionId": request.session.session_key if request.session.session_key else None,
#                 "responseMessage": "system failure, retry",
#                 "responseCode": "03"
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)

class AdminTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticated]

# class TransactionView(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     # permission_classes = [IsAuthenticated]


from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from account.models import Transaction
from account.serializers import TransactionSerializer
import logging

logger = logging.getLogger(__name__)

# class TransactionView(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     # Temporarily remove authentication
#     # permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         try:
#             # Log the request data and headers for debugging
#             logger.debug(f"Request data: {request.data}")
#             logger.debug(f"Request headers: {request.headers}")

#             # Extracting data from the request body
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             request_data = request.data

#             # Extracting required fields
#             sessionId = request.session.session_key  # Using the session key
#             settlementId = request_data.get("settlementId")
#             x_auth_signature = request.headers.get("X-Auth-Signature")
#             logger.debug(f"Session ID: {sessionId}")
#             logger.debug(f"Settlement ID: {settlementId}")
#             logger.debug(f"X-Auth-Signature: {x_auth_signature}")

#             # Expected X-auth-Signature
#             expected_signature = "BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7"

#             # Check for missing required data
#             if not sessionId or not settlementId:
#                 logger.warning("Missing required fields")
#                 return JsonResponse({
#                     "requestSuccessful": True,
#                     "sessionId": str(sessionId),
#                     "responseMessage": "rejected transaction",
#                     "responseCode": "02"
#                 })

#             # Check if the X-auth-Signature matches the expected value
#             if x_auth_signature != expected_signature:
#                 logger.warning("Invalid X-Auth-Signature")
#                 return JsonResponse({
#                     "requestSuccessful": True,
#                     "sessionId": str(sessionId),
#                     "responseMessage": "rejected transaction",
#                     "responseCode": "02"
#                 })

#             # Check for duplicate settlementId
#             if Transaction.objects.filter(settlementId=settlementId).exists():
#                 logger.warning("Duplicate settlementId")
#                 return JsonResponse({
#                     "requestSuccessful": True,
#                     "sessionId": str(sessionId),
#                     "responseMessage": "duplicate transaction",
#                     "responseCode": "01"
#                 })

#             # Include the account number in the transaction data
#             transaction_data = serializer.validated_data
#             transaction_data['accountNumber'] = request.user.account_number if request.user.is_authenticated else None

#             # Create the transaction
#             transaction = Transaction.objects.create(**transaction_data)
#             serializer = self.get_serializer(transaction)
#             headers = self.get_success_headers(serializer.data)
#             logger.info("Transaction created successfully")

#             return Response({
#                 "requestSuccessful": True,
#                 "sessionId": str(sessionId),
#                 "responseMessage": "success",
#                 "responseCode": "00"
#             }, status=status.HTTP_201_CREATED, headers=headers)

#         except Exception as e:
#             logger.error(f"Exception in creating transaction: {str(e)}", exc_info=True)
#             return JsonResponse({
#                 "requestSuccessful": True,
#                 "sessionId": request.session.session_key if request.session.session_key else None,
#                 "responseMessage": "system failure, retry",
#                 "responseCode": "03"
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Transaction
from .serializers import TransactionSerializer
import logging

logger = logging.getLogger(__name__)

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class TransactionView(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    # Temporarily remove authentication
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            # Log the request data and headers for debugging
            logger.debug(f"Request data: {request.data}")
            logger.debug(f"Request headers: {request.headers}")

            # Extracting data from the request body
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            request_data = serializer.validated_data

            # Extracting required fields
            sessionId = request_data.get("sessionId")
            settlementId = request_data.get("settlementId")
            accountNumber = request_data.get("accountNumber")
            x_auth_signature = request.headers.get("X-Auth-Signature")
            logger.debug(f"Session ID: {sessionId}")
            logger.debug(f"Settlement ID: {settlementId}")
            logger.debug(f"X-Auth-Signature: {x_auth_signature}")

            # Expected X-auth-Signature
            expected_signature = "BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7"

            # Check if the X-auth-Signature is missing or incorrect
            if x_auth_signature != expected_signature:
                logger.warning("Missing or invalid X-Auth-Signature")
                return JsonResponse({
                    "requestSuccessful": True,
                    "sessionId": str(sessionId) if sessionId else None,
                    "responseMessage": "rejected transaction",
                    "responseCode": "02"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check for missing required data
            if not accountNumber or not settlementId:
                logger.warning("Missing required fields")
                return JsonResponse({
                    "requestSuccessful": True,
                    "sessionId": str(sessionId) if sessionId else None,
                    "responseMessage": "rejected transaction",
                    "responseCode": "02"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check for duplicate settlementId
            if Transaction.objects.filter(settlementId=settlementId).exists():
                logger.warning("Duplicate settlementId")
                return JsonResponse({
                    "requestSuccessful": True,
                    "sessionId": str(sessionId),
                    "responseMessage": "duplicate transaction",
                    "responseCode": "01"
                }, status=status.HTTP_200_OK)

            # Create the transaction
            transaction = Transaction.objects.create(**request_data)
            serializer = self.get_serializer(transaction)
            headers = self.get_success_headers(serializer.data)
            logger.info("Transaction created successfully")

            return Response({
                "requestSuccessful": True,
                "sessionId": str(sessionId),
                "responseMessage": "success",
                "responseCode": "00"
            }, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            logger.error(f"Exception in creating transaction: {str(e)}", exc_info=True)
            return JsonResponse({
                "requestSuccessful": True,
                "sessionId": request.data.get("sessionId") if request.data.get("sessionId") else None,
                "responseMessage": "system failure, retry",
                "responseCode": "03"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

