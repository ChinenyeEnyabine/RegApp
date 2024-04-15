from django.shortcuts import render
from rest_framework import viewsets
from transactional.models import TransactionWithUser
from transactional.serializers import TransactionalSerializer

class TransactionalViewSet(viewsets.ModelViewSet):
    queryset=TransactionWithUser.objects.all()
    serializer_class=TransactionalSerializer
