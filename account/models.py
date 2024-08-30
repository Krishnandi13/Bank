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
    account_number=models.CharField(max_length=20)
    owner_name=models.CharField(max_length=100)
    status=models.CharField(max_length=10,choices=STATUS_CHOICE,default='OPEN')
    
   
class transaction(models.Model):
    TRANSACTION_TYPE=[
        ('DEPOSIT','Deposit'),
        ('WITHDRAWAL','Withdrawl'),
        ('TRANSFER','Transfer'),
    ]
    
    STATUS_CHOICE=[
         ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    transaction_id=models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    account=models.ForeignKey(to=Account,on_delete=models.CASCADE)
    transaction_type=models.CharField(max_length=10,choices=TRANSACTION_TYPE)
    transaction_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICE,default='PENDING')
    
    
    