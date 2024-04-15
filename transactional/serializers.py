
from rest_framework import serializers

from transactional.models import TransactionWithUser
class TransactionalSerializer(serializers.ModelSerializer):
    class Meta:
        model=TransactionWithUser
        fields="__all__"
    
    