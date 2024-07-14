# # serializers.py

# from rest_framework import serializers
# # from .models import BillOperation, UtilityOrder

# class BillOperationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BillOperation
#         fields = '__all__'

# class UtilityOrderSerializer(serializers.ModelSerializer):
#     utility = BillOperationSerializer()

#     class Meta:
#         model = UtilityOrder
#         fields = '__all__'

#     def create(self, validated_data):
#         utility_data = validated_data.pop('utility')
#         utility = BillOperation.objects.create(**utility_data)
#         order = UtilityOrder.objects.create(utility=utility, **validated_data)
#         return order
from rest_framework import serializers
from .models import Transaction, AirtimeBundle, DataBundle

class AirtimeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'transaction_type', 'airtime_bundle', 'phone_number', 'transaction_date', 'transaction_status', 'transaction_id']
        read_only_fields = ['transaction_date', 'transaction_status', 'transaction_id']
    
    def create(self, validated_data):
        validated_data['transaction_type'] = 'AIRTIME'
        return super().create(validated_data)

class DataTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'transaction_type', 'data_bundle', 'phone_number', 'transaction_date', 'transaction_status', 'transaction_id']
        read_only_fields = ['transaction_date', 'transaction_status', 'transaction_id']

    def create(self, validated_data):
        validated_data['transaction_type'] = 'DATA'
        return super().create(validated_data)
