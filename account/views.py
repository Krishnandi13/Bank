from decimal import Decimal
from urllib import request
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
from datetime import datetime
from django.utils.dateparse import parse_date

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
        import ipdb;ipdb.set_trace()
        accounts=Account.objects.all()
        # serializer=AccountSerializer(accounts,many=True)
        account_list = []
        for account in accounts:
            account_data = {
                "account_number":account.account_number,
                "owner_name":account.owner_name,
                "status":account.status,
                "balance":account.balance
            }
            account_list.append(account_data)
        return Response(account_list)

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
            transaction_type=request.query_params.get('transaction_type')
            start_date=request.query_params.get('start_date')
            end_date=request.query_params.get('end_date')

            if not account_number:
                return Response({"error": "Account number is required."}, status=status.HTTP_400_BAD_REQUEST)
        
            account=Account.objects.get(account_number=account_number)

            transactions=Transaction.objects.filter(account=account)
            
            
            if transaction_type:
                transactions=Transaction.objects.filter(transaction_type=transaction_type)
                
                
            if start_date and end_date:
                try:
                    start_date = parse_date(start_date)
                    end_date = parse_date(end_date)  
                    
                    transactions=Transaction.objects.filter(transaction_date__range=[start_date,end_date])

                except ValueError:
                     return Response({"error": "Invalid date format. Use 'YYYY-MM-DD'."}, status=status.HTTP_400_BAD_REQUEST)
                    
                
                
            serializer=TransactionSerializer(transactions,many=True)
        
            return Response(serializer.data)
        
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND) 
            
    
class AccountToAccount(APIView):
    
    def post(self,request):
        
        account_number_1=request.query_params.get('account_number_1')
        account_number_2=request.query_params.get('account_number_2')
        amount=request.query_params.get('amount')
        
        if not account_number_1 or not account_number_1 or not amount:
            return Response({"error": "account_number_1,account_number_2 and Amount is required as a query parameter."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            amount=Decimal(amount)
            if amount<=0:
                return Response({"error": "The amount transfer should be positive"}, status=status.HTTP_400_BAD_REQUEST)
             
            
            account_1 = Account.objects.get(account_number=account_number_1)  
            account_2 = Account.objects.get(account_number=account_number_2)
            
            if account_1.status=='CLOSE' or account_2.status=='CLOSE':
                return Response({"error": "one or both account is/are closed."}, status=status.HTTP_400_BAD_REQUEST)
            
            if account_1.balance<amount:
                return Response({'msg':'Insufficient balance '},status=status.HTTP_400_BAD_REQUEST)
            account_1.balance-=amount
            account_1.save()
            
            account_2.balance+=amount
            account_2.save()
            
            Transaction.objects.create(
                account=account_1,
                transaction_type='TRANSFER',
                amount=amount,
                origin_account_number=account_number_1,
                destination_account_number=account_number_2,
            )
            
            Transaction.objects.create(
                account=account_2,
                transaction_type='TRANSFER',
                amount=amount,
                origin_account_number=account_number_1,
                destination_account_number=account_number_2
                
            )
            return Response({'msg':' Amount Transafered Successfully'},status=status.HTTP_200_OK)
        
        except ValueError:
            return Response({"error": "Invalid amount provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Account.DoesNotExist:
            return Response({'msg':'Account doesnt exist'},status=status.HTTP_200_OK)    
                
            
            
        