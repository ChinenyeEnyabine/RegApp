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



from rest_framework.permissions import IsAuthenticated



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


# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from django.http import JsonResponse
# from .models import Transaction
# from .serializers import TransactionSerializer
# import logging

# logger = logging.getLogger(__name__)

# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from django.http import JsonResponse
# import logging

# logger = logging.getLogger(__name__)

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
#             request_data = serializer.validated_data

#             # Extracting required fields
#             sessionId = request_data.get("sessionId")
#             settlementId = request_data.get("settlementId")
#             accountNumber = request_data.get("accountNumber")
#             x_auth_signature = request.headers.get("X-Auth-Signature")
#             logger.debug(f"Session ID: {sessionId}")
#             logger.debug(f"Settlement ID: {settlementId}")
#             logger.debug(f"X-Auth-Signature: {x_auth_signature}")

#             # Expected X-auth-Signature
#             expected_signature = "BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7"

#             # Check if the X-auth-Signature is missing or incorrect
#             if x_auth_signature != expected_signature:
#                 logger.warning("Missing or invalid X-Auth-Signature")
#                 return JsonResponse({
#                     "requestSuccessful": True,
#                     "sessionId": str(sessionId) if sessionId else None,
#                     "responseMessage": "rejected transaction",
#                     "responseCode": "02"
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Check for missing required data
#             if not accountNumber or not settlementId:
#                 logger.warning("Missing required fields")
#                 return JsonResponse({
#                     "requestSuccessful": True,
#                     "sessionId": str(sessionId) if sessionId else None,
#                     "responseMessage": "rejected transaction",
#                     "responseCode": "02"
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Check for duplicate settlementId
#             if Transaction.objects.filter(settlementId=settlementId).exists():
#                 logger.warning("Duplicate settlementId")
#                 return JsonResponse({
#                     "requestSuccessful": True,
#                     "sessionId": str(sessionId),
#                     "responseMessage": "duplicate transaction",
#                     "responseCode": "01"
#                 }, status=status.HTTP_200_OK)

#             # Create the transaction
#             transaction = Transaction.objects.create(**request_data)
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
#                 "sessionId": request.data.get("sessionId") if request.data.get("sessionId") else None,
#                 "responseMessage": "system failure, retry",
#                 "responseCode": "03"
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

##############################################################################################
########################################################################################

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Transaction, User
from .serializers import TransactionSerializer
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

            # Check if the accountNumber exists in the User model
            if not User.objects.filter(account_number=accountNumber).exists():
                logger.warning("Invalid accountNumber")
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

