from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.utils import timezone

class User(AbstractUser):
    fullname = models.CharField(max_length=255, default=True)
    email = models.EmailField(max_length=255, unique=True)
    role = models.TextField()
    first_name = models.CharField(max_length=255, default=True)
    last_name = models.CharField(max_length=255, default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

class Warehouse(models.Model):
    warehousename = models.CharField(max_length=255)
    warehousecode = models.CharField(primary_key=True, max_length=255)
    warehousetype = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class User_Warehouse(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,related_name='user_warehouse')
    warehouse = models.ForeignKey(Warehouse, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class IcgSaleTransactions(models.Model):
    #warehousecode = models.ForeignKey(Warehouse, on_delete=models.CASCADE,max_length=255)
    warehousecode = models.CharField(max_length=255,null=True)
    icgtransactionscode = models.CharField(max_length=255,null=True, unique=True)
    paymenttype = models.CharField(max_length=255)
    transactiondate = models.DateTimeField()
    amount =models.DecimalField(max_digits=20, decimal_places=4,default=0.0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class ReconcileSaleTransactions(models.Model):
    #warehousecode = models.ForeignKey(Warehouse, on_delete=models.CASCADE,max_length=255)
    reconciletransactionscode = models.CharField(max_length=255,null=True, unique=True)
    paymenttype = models.CharField(max_length=255)
    settlement_amount =models.DecimalField(max_digits=20, decimal_places=4,default=0.0) 
    bank_amount =models.DecimalField(max_digits=20, decimal_places=4,default=0.0) 
    is_reconcile = models.BooleanField(default=True)
    transactiondate = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class LogEntry(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='log_entries')
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    def __str__(self):
        return f"{self.timestamp} - {self.user.username if self.user else 'Anonymous'}: {self.message}"

