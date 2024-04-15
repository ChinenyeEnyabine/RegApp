from account.models import Transaction, User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
class LoginSerializer(serializers.ModelSerializer):
     class Meta:
        model = User       
        exclude = ('password',)
        read_only_fields = ('id',)



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = "__all__"
        # extra_kwargs = {
        #     'first_name': {'required': True},
        #     'last_name': {'required': True}
        # }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user =User.objects.create(
            
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            account_number=validated_data['account_number'],
            phone_number=validated_data['phone_number'],
            photo=validated_data['photo'],
            
    
        )
        user.set_password(validated_data['password'])
        user.save()

        return user        
# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = '__all__'


from rest_framework import serializers
from .models import Transaction,User

#
        
#         return transaction
from rest_framework import serializers
from .models import Transaction

# class TransactionSerializer(serializers.ModelSerializer):
#     account_number = serializers.CharField(source='User.account_number')

#     class Meta:
#         model = Transaction
#         fields = ['sessionId', 'initiationTranRef', 'tranRemarks', 'transactionAmount', 'settledAmount', 'feeAmount', 'vatAmount', 'currency', 'settlementId', 'sourceAccountNumber', 'sourceAccountName', 'sourceBankName', 'channelId', 'tranDateTime', 'account_number']

#     def create(self, validated_data):
#         # Extract user from validated_data
#         user_data = validated_data.pop('User')
#         # Extract account_number from user_data
#         account_number = user_data.get('account_number')

#         # Create the Transaction object with the extracted account_number
#         transaction = Transaction.objects.create(account_number=account_number, **validated_data)
        
#         return transaction
    
# from rest_framework import serializers
# from .models import Transaction

# class TransactionSerializer(serializers.ModelSerializer):
#     account_number = serializers.CharField(source='user.account_number', read_only=True)

#     class Meta:
#         model = Transaction
#         fields = ['id','sessionId', 'initiationTranRef', 'tranRemarks', 'transactionAmount', 'settledAmount', 'feeAmount', 'vatAmount', 'currency', 'settlementId', 'sourceAccountNumber', 'sourceAccountName', 'sourceBankName', 'channelId', 'tranDateTime', 'account_number']
#         read_only_fields = ['id']  # Ensure id field is read-only

#     def create(self, validated_data):
#         return Transaction.objects.create(**validated_data)
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        settlement_id = validated_data.get('settlementId')
        existing_transaction = Transaction.objects.filter(settlementId=settlement_id).exists()
        
        if existing_transaction:
            raise serializers.ValidationError("Transaction with this settlementId already exists.")
        
        return Transaction.objects.create(**validated_data)
