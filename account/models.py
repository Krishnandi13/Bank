from django.db import models
import uuid
from customer.models import Customer
from product_catalog.models import Product


# Create your models here.
class Account(models.Model):
    STATUS_CHOICE=[
        ('OPEN','Open Account'),
        ('CLOSE','Close Account'),
    ]
    
    product=models.ForeignKey(to=Product,on_delete=models.PROTECT)
    customer=models.ForeignKey(to=Customer,on_delete=models.CASCADE)
    account_number=models.CharField(max_length=20,unique=True)
    owner_name=models.CharField(max_length=100)
    status=models.CharField(max_length=10,choices=STATUS_CHOICE,default='OPEN')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    
    def __str__(self):
        return f"{self.product} {self.customer},{self.account_number},{self.owner_name},{self.status}"
   
class Transaction(models.Model):
    TRANSACTION_TYPE=[
        ('DEPOSIT','Deposit'),
        ('WITHDRAWAL','Withdrawl'),
        ('TRANSFER','Transfer'),
    ]
    
    
    
    transaction_id=models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    account=models.ForeignKey(to=Account,on_delete=models.CASCADE)
    transaction_type=models.CharField(max_length=10,choices=TRANSACTION_TYPE)
    transaction_date=models.DateTimeField(auto_now_add=True)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    
    
    