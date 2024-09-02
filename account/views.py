from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import account
from account import serializer
from account.serializer import  CreateAccountSerializer,AccountSerializer,CreateTransactionSerializer,TransactionSerializer
from customer.models import Customer
from product_catalog.models import Product
from account.models import Account,Transaction
import random

# Create your views here.

class CreateAccountApi(APIView):
    
    def post(self,request):
        
        serializer=CreateAccountSerializer(data=request.data)
        try:
            if serializer.is_valid():
                validatedData=serializer.validated_data
                email=validatedData.get('email')
                product_name=validatedData.get('product_name')
            
                customer=Customer.objects.get(email=email)
                product=Product.objects.get(product_name=product_name)
                
                account=Account.objects.create(
                    customer=customer,
                    product=product,
                    account_number=random.randint(1000000000,9999999999),
                    owner_name=f"{customer.first_name} {customer.last_name}"
                )
                return Response({'msg':'Account CREATED'},status=status.HTTP_201_CREATED)    
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Customer.DoesNotExist :
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
            
class GetAllAccounts(APIView):
    
    def get(self,request):
        
        accounts=Account.objects.all()
        serializer=AccountSerializer(accounts,many=True)
        return Response(serializer.data)

class GetOneAccount(APIView):
    
    
    def get(self,request):
        
            account_number=request.query_params.get('account_number')
        
            if not account_number:
                return Response({"error": " account_number  parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                account=Account.objects.get(account_number=account_number)
                
            except Account.DoesNotExist :
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)  
            
            serializer=AccountSerializer(account)
            return Response(serializer.data) 
        
class CloseAccountApi(APIView):
    
    def put(self,request):
        
        account_number=request.query_params.get('account_number')
        if not account_number:
            return Response({"error": "account_number is required as a query parameter."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            account=Account.objects.get(account_number=account_number)   
            if account.status!='CLOSE':
                account.status='CLOSE'
                account.save()
                return Response({"message": "Account closed successfully"}, status=status.HTTP_200_OK) 
            
            else:
                return Response({"message": "Account is already closed"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        

class DepositApi(APIView):
    
    def post(self,request):
        
        serializer=CreateTransactionSerializer(data=request.data)
        try:
            if serializer.is_valid():
                validatedData=serializer.validated_data
                account_number=validatedData.get('account_number')
                amount=validatedData.get('amount')
            
                account=Account.objects.get(account_number=account_number)
                account.balance+=amount
                
                account.save()
                tranasaction=Transaction.objects.create(
                    account=account,
                    transaction_type='DEPOSIT',
                    amount=amount
                    
                )
                return Response({'msg':'Deposited'},status=status.HTTP_200_OK)    
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        

class WithdrawApi(APIView):
    
    def post(self,request):
        
        serializer=CreateTransactionSerializer(data=request.data)
        try:
            if serializer.is_valid():
                validatedData=serializer.validated_data
                account_number=validatedData.get('account_number')
                amount=validatedData.get('amount')
            
                account=Account.objects.get(account_number=account_number)
                if account.balance<amount:
                    return Response({'msg':'Insufficient balance '},status=status.HTTP_400_BAD_REQUEST) 
                account.balance-=amount
                
                account.save()
                tranasaction=Transaction.objects.create(
                    account=account,
                    transaction_type='WITHDRAWAL',
                    amount=amount
                    
                )
                return Response({'msg':'Withdrawed'},status=status.HTTP_200_OK)    
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)  
              
class TransactionStatement(APIView) :
    
    def get(self,request):
        
        try:
            
            account_number=request.query_params.get('account_number')
        
            account=Account.objects.get(account_number=account_number)

            transactions=Transaction.objects.filter(account=account)
        
            serializer=TransactionSerializer(transactions,many=True)
        
            return Response(serializer.data)
        
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND) 
            
    
        
               
        