# from django.db import models
# from django.contrib.auth.models import AbstractUser


# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class Skisubuser(AbstractUser):
#     phone = models.CharField(max_length=14)
#     created_date = models.DateField(auto_now_add=True)
#     updated_date = models.DateField(auto_now=True)
    
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Skisubuser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=14)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    account_number=models.CharField(max_length=20, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # Optionally, set email as the primary key for uniqueness.
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.email


    # status=models.CharField(max_length=20,default='Pending')
    # is_active=models.BooleanField(default=False)
    # is_staff=models.BooleanField(default=False)
    # is_user=models.BooleanField(default=False),
    # is_admin=models.BooleanField(default=False)
    

    def __str__(self):
        return self.email
    
# models.py



@receiver(post_save, sender=Skisubuser)
def set_account_number(sender, instance, created, **kwargs):
    if created:
        # Prepare the payload for the API request using signup data
        payload = {
           'account_name': instance.first_name + ' ' + instance.last_name,
            
            # Add other fields as needed...
        }
        headers = {
            'Client-Id': 'dGVzdF9Qcm92aWR1cw==',
            'X-Auth-Signature': 'BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7',
            'Content-Type': 'application/json',  # Assuming JSON API
        }
        # Make a POST request to the API
        response = requests.post('http://154.113.16.142:8088/appdevapi/api/PiPCreateDynamicAccountNumber', json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Extract the account number from the response
            account_number = response.json().get('account_number')
            
            # Update the corresponding UserSignup instance with the account number
            instance.account_number = account_number
            instance.save()





class Transaction(models.Model):
    user = models.ForeignKey(Skisubuser, on_delete=models.CASCADE, related_name='transactions')
    sessionId = models.CharField(max_length=50)
    initiationTranRef = models.CharField(max_length=50, blank=True)
    accountNumber = models.CharField(max_length=20)
    tranRemarks = models.CharField(max_length=255, blank=True)
    transactionAmount = models.DecimalField(max_digits=15, decimal_places=2)
    settledAmount = models.DecimalField(max_digits=15, decimal_places=2)
    feeAmount = models.DecimalField(max_digits=15, decimal_places=2)
    vatAmount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3)
    settlementId = models.CharField(max_length=50)
    sourceAccountNumber = models.CharField(max_length=20, blank=True)
    sourceAccountName = models.CharField(max_length=255, blank=True)
    sourceBankName = models.CharField(max_length=255, blank=True)
    channelId = models.CharField(max_length=50, blank=True)
    tranDateTime = models.DateTimeField()

    def __str__(self):
        return self.sessionId

