from rest_framework import serializers
from account import models
from account.models import Account, Transaction
from customer.serializer import CustomerSerializer
from product_catalog.serializer import ProductSerializer


class CreateAccountSerializer(serializers.Serializer):
   
    email=serializers.EmailField()
    product_name=serializers.CharField(max_length=20)
    
class AccountSerializer(serializers.ModelSerializer):
    
    customer = CustomerSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model=Account
        fields=['customer','product','account_number','owner_name','status','balance']    
        
        
class CreateTransactionSerializer(serializers.Serializer):
    account_number=serializers.CharField(max_length=20)
    amount=serializers.DecimalField(max_digits=10,decimal_places=2)
    
class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Transaction
        fields=['transaction_id','account','transaction_type','transaction_date','amount']          