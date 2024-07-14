# # models.py

# from django.db import models
# from account.models import User

# class BillOperation(models.Model):
#     BILL_TYPES = (
#         ("recharge_card", "recharge_card"),
#         ("data", "data"),
#         ("electricity", "electricity"),
#         ("cabletv", "cabletv"),
#     )
#     SERVICE_TYPES = (
#         ("mtn", "mtn"),
#         ("globacom", "globacom"),
#         ("airtel", "airtel"),
#         ("9mobile", "9mobile"),
#     )
#     ELECTRICITY_PROVIDERS = (
#         ("ibedc", "ibedc"),
#         ("aedc", "aedc"),
#         ("ieelectric", "ieelectric"),
#         ("ekodisco", "ekodisco"),
#     )
#     CABLETV_PROVIDERS = (
#         ("dstv", "dstv"),
#         ("gotv", "gotv"),
#         ("showmax", "showmax"),
#         ("startimes", "startimes"),
#     )
#     DSTV_BOUQUETS = (
#         ("binja", "binja"),
#         ("labe", "labe"),
#         # Add other DSTV bouquets here
#     )
#     GOTV_BOUQUETS = (
#         ("jinja", "jinja"),
#         ("joli max", "joli max"),
#         # Add other GOTV bouquets here
#     )
#     SHOWMAX_BOUQUETS = (
#         # Add Showmax bouquets here
#         ("jinja", "jinja"),
#         ("joli max", "joli max"),
#     )
#     STARTIMES_BOUQUETS = (
#         # Add Startimes bouquets here
#         ("jinja", "jinja"),
#         ("joli max", "joli max"),
#     )

#     bill_class = models.CharField(max_length=250, choices=BILL_TYPES, default='data', null=True, blank=True)
#     phone_no = models.CharField(max_length=14, null=True, blank=True)
#     service_ops = models.CharField(max_length=100, null=True, blank=True)
#     amount = models.IntegerField(null=True, blank=True)
#     dataplan = models.CharField(max_length=200, null=True, blank=True)
#     rechargeplan = models.CharField(max_length=200, null=True, blank=True)
#     meterno = models.CharField(max_length=100, null=True, blank=True)
#     smart_card = models.CharField(max_length=100, null=True, blank=True)
#     selectbouquet = models.CharField(max_length=100, null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if self.bill_class == "recharge_card" or self.bill_class == "data":
#             self.service_ops = models.CharField(max_length=100, choices=self.SERVICE_TYPES, null=True, blank=True)
#         elif self.bill_class == "electricity":
#             self.service_ops = models.CharField(max_length=100, choices=self.ELECTRICITY_PROVIDERS, null=True, blank=True)
#         elif self.bill_class == "cabletv":
#             if self.service_ops == "dstv":
#                 self.selectbouquet = models.CharField(max_length=100, choices=self.DSTV_BOUQUETS, null=True, blank=True)
#             elif self.service_ops == "gotv":
#                 self.selectbouquet = models.CharField(max_length=100, choices=self.GOTV_BOUQUETS, null=True, blank=True)
#             elif self.service_ops == "showmax":
#                 self.selectbouquet = models.CharField(max_length=100, choices=self.SHOWMAX_BOUQUETS, null=True, blank=True)
#             elif self.service_ops == "startimes":
#                 self.selectbouquet = models.CharField(max_length=100, choices=self.STARTIMES_BOUQUETS, null=True, blank=True)
#         super().save(*args, **kwargs)

# class UtilityOrder(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     utility = models.ForeignKey(BillOperation, on_delete=models.CASCADE)
#     order_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"Order {self.id} - {self.user.username}"
import uuid
from django.db import models
from account.models import User

class ServiceProvider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)  # For identifying the provider in transactions

    def __str__(self):
        return self.name

class AirtimeBundle(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='airtime_bundles')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Adjust max_digits and decimal_places as necessary

    def __str__(self):
        return f"{self.service_provider.name} - {self.name} (Airtime)"

class DataBundle(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='data_bundles')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Adjust max_digits and decimal_places as necessary
    data_volume = models.CharField(max_length=50)  # e.g., '1GB', '500MB'
    validity_period = models.CharField(max_length=50)  # e.g., '30 days', '7 days'

    def __str__(self):
        return f"{self.service_provider.name} - {self.name} (Data)"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('AIRTIME', 'Airtime'),
        ('DATA', 'Data'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    airtime_bundle = models.ForeignKey(AirtimeBundle, null=True, blank=True, on_delete=models.CASCADE)
    data_bundle = models.ForeignKey(DataBundle, null=True, blank=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=20, default='Pending')  # Pending, Success, Failed
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
   

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.phone_number}"

    class Meta:
        ordering = ['-transaction_date']
