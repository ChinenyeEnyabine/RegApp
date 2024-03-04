from skisub.models import BillOperation
from rest_framework import serializers

class AirtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model=BillOperation
        fields=['billclass','serviceops','phone','amount','rechargeplan']
    def create(self,validated_data):
        airtime=BillOperation.objects.create(
            billclass=validated_data['billclass'],
            serviceops=validated_data['serviceops'],
            phone=validated_data['phone'],
            amount=validated_data['amount'],
            rechargeplan=validated_data['rechargeplan']
        )
        return airtime

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model=BillOperation
        fields=['billclass','serviceops','phone','amount','dataplan']
    def create(self,validated_data):
        data=BillOperation.objects.create(
            billclass=validated_data['billclass'],
            serviceops=validated_data['serviceops'],
            phone=validated_data['phone'],
            amount=validated_data['amount'],
            dataplan=validated_data['dataplan']
        )
        return data

class CabletvSerializer(serializers.ModelSerializer):
    class Meta:
        model=BillOperation
        fields=['category','serviceops','smart_card','selectbouquet']
        def create(self,validated_data):
            cable=BillOperation.objects.create(
               category=validated_data['category'],
               serviceops=validated_data['serviceops'],
               smart_card=validated_data['smart_card'],
               selectbouquet=validated_data['selectbouquet']
            )
            return cable


class ElectricitySerializer(serializers.ModelSerializer):
    class Meta:
        model=BillOperation
        fields=['category','serviceops','meterno']
        def create(self,validated_data):
            electricity=BillOperation.objects.create(
               category=validated_data['category'],
               serviceops=validated_data['serviceops'],
               meterno=validated_data['meterno']
            )
            return electricity
