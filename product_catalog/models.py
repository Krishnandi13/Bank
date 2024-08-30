from django.db import models

# Create your models here.
class Product(models.Model):
    PRODUCT_TYPES=[
        ('SAVINGS','Savings Account'),
        ('CURRENT','Current Account'),
        ('DEBIT','Debit Card'),
        ('CREDIT','Credit Card'),
    ]
    
    
    
    product_type=models.CharField(max_length=10,choices=PRODUCT_TYPES)
    product_name=models.CharField(max_length=20)
    description=models.TextField(null=True,blank=False)