from django.db import models

from account.models import Transaction, User

# Create your models here.
class TransactionWithUser(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)