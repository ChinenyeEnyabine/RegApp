# from account.models import Transaction, User
# from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
# from django.contrib.auth.password_validation import validate_password
# class LoginSerializer(serializers.ModelSerializer):
#      class Meta:
#         model = User       
#         exclude = ('password',)
#         read_only_fields = ('id',)



# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#             required=True,
#             validators=[UniqueValidator(queryset=User.objects.all())]
#             )

#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = "__all__"
#         # extra_kwargs = {
#         #     'first_name': {'required': True},
#         #     'last_name': {'required': True}
#         # }

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})

#         return attrs

#     def create(self, validated_data):
#         user =User.objects.create(
            
#             email=validated_data['email'],
#             username=validated_data['username'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             account_number=validated_data['account_number'],
#             phone_number=validated_data['phone_number'],
#             photo=validated_data['photo'],
            
    
#         )
#         user.set_password(validated_data['password'])
#         user.save()

#         return user        



from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from account.models import Transaction, User
import requests

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

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            photo=validated_data.get('photo'),
        )
        user.set_password(validated_data['password'])
        user.save()

        # Prepare the payload for the API request using signup data
        payload = {
            'account_name': user.first_name + ' ' + user.last_name,
        }
        headers = {
            'Client-Id': 'dGVzdF9Qcm92aWR1cw==',
            'X-Auth-Signature': 'BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7',
            'Content-Type': 'application/json',
        }
        response = requests.post('http://154.113.16.142:8088/appdevapi/api/PiPCreateDynamicAccountNumber', json=payload, headers=headers)
        
        if response.status_code == 200:
            account_number = response.json().get('account_number')
            user.account_number = account_number
            user.save()

        return user
# serializers.py

# serializers.py

# import threading
# import requests
# import logging
# from retry import retry
# from django.core.exceptions import ObjectDoesNotExist
# from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
# from django.contrib.auth.password_validation import validate_password
# from account.models import User

# logger = logging.getLogger(__name__)

# # In your serializers.py

# from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.password_validation import validate_password
# from .models import User
# import threading
# import requests
# import logging

# logger = logging.getLogger(__name__)

# def fetch_account_number(user_id):
#     """
#     Fetches the account number for a given user and updates the user's account number field.
#     """
#     try:
#         user = User.objects.get(id=user_id)
#         payload = {
#             'account_name': f"{user.first_name} {user.last_name}",
#         }
#         headers = {
#             'Client-Id': 'dGVzdF9Qcm92aWR1cw==',
#             'X-Auth-Signature': 'BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7',
#             'Content-Type': 'application/json',
#         }

#         response = requests.post(
#             'http://154.113.16.142:8088/appdevapi/api/PiPCreateDynamicAccountNumber',
#             json=payload,
#             headers=headers
#         )

#         logger.debug(f"API Response: {response.status_code} - {response.text}")

#         if response.status_code == 200:
#             response_data = response.json()

#             account_number = response_data.get('account_number')

#             if account_number:
#                 user.account_number = account_number
#                 user.save()
#                 logger.info(f"Account number {account_number} created for user {user.email}")
#                 # Optionally send a notification to the user here
#             else:
#                 logger.error(f"Account number not returned for user {user.email}. Response: {response_data}")
#         else:
#             logger.error(f"Failed to fetch account number for user {user.email}. Status code: {response.status_code}, Response: {response.text}")

#     except ObjectDoesNotExist:
#         logger.error(f"User with ID {user_id} does not exist")
#     except requests.RequestException as e:
#         logger.error(f"Request failed for user with ID {user_id}: {str(e)}")
#     except Exception as e:
#         logger.error(f"Unexpected error for user with ID {user_id}: {str(e)}")

# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'photo', 'password', 'password2']

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#         return attrs

#     def create(self, validated_data):
#         # Create the user
#         user = User.objects.create(
#             email=validated_data['email'],
#             username=validated_data['username'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             phone_number=validated_data['phone_number'],
#             photo=validated_data.get('photo'),
#         )
#         user.set_password(validated_data['password'])
#         user.save()

#         # Run the account number fetcher in a separate thread
#         thread = threading.Thread(target=fetch_account_number, args=(user.id,))
#         thread.start()

#         return user





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class TransactionSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.email')

#     class Meta:
#         model = Transaction
#         fields = '__all__'
from rest_framework import serializers
from account.models import Transaction
import logging

logger = logging.getLogger(__name__)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'  # or list specific field

    accountNumber = serializers.CharField(required=False, allow_blank=True)
    settlementId = serializers.CharField(required=False, allow_blank=True)

    # def validate(self, data):
    #     request = self.context.get('request')
    #     sessionId = request.session.session_key
    #     settlementId = data.get('settlementId')
    #     x_auth_signature = request.headers.get("X-Auth-Signature")
    #     expected_signature = "BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7"

    #     logger.debug(f"Request data: {data}")
    #     logger.debug(f"Session ID: {sessionId}")
    #     logger.debug(f"Settlement ID: {settlementId}")
    #     logger.debug(f"X-Auth-Signature: {x_auth_signature}")

    #     if not sessionId or not settlementId:
    #         logger.warning("Missing required fields")
    #         raise serializers.ValidationError({
    #             "requestSuccessful": True,
    #             "sessionId": str(sessionId),
    #             "responseMessage": "rejected transaction",
    #             "responseCode": "02"
    #         })

    #     if x_auth_signature != expected_signature:
    #         logger.warning("Invalid X-Auth-Signature")
    #         raise serializers.ValidationError({
    #             "requestSuccessful": True,
    #             "sessionId": str(sessionId),
    #             "responseMessage": "rejected transaction",
    #             "responseCode": "02"
    #         })

    #     if Transaction.objects.filter(settlementId=settlementId).exists():
    #         logger.warning("Duplicate settlementId")
    #         raise serializers.ValidationError({
    #             "requestSuccessful": True,
    #             "sessionId": str(sessionId),
    #             "responseMessage": "duplicate transaction",
    #             "responseCode": "01"
    #         })

    #     return data

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user = request.user
    #     transaction = Transaction.objects.create(user=user, **validated_data)
    #     logger.info("Transaction created successfully")
    #     return transaction
