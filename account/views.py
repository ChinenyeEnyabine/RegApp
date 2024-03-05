from django.shortcuts import render
from rest_framework.views import APIView
from knox.models import AuthToken
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import  login
from rest_framework.response import Response

from account.models import User, Transaction
from rest_framework import status
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

class TransactionListCreateView(APIView):
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)