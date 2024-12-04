from ast import Delete, Return
from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from account import serializer
import customer
from customer.models import Customer
from customer.serializer import CustomerSerializer
from rest_framework.views import APIView
from rest_framework import status

class CreateCustomerAPI(APIView):
    
    def post(self,request):
        
        serializer=CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'DATA CREATED'},status=status.HTTP_201_CREATED)    
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GetAllCustomerApi(APIView):
    
    def get(self,request):
        
        customers=Customer.objects.all()
        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data)
    
class GetOneCustomerApi(APIView):
    
    def get(self,request):
        email=request.query_params.get('email')
        
        if not email:
            return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            customer=Customer.objects.get(email=email)
            
        except Customer.DoesNotExist :
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)  
         
        serializer=CustomerSerializer(customer)
        return Response(serializer.data) 
            
class UpdateOneCustomerApi(APIView):
    
    def put(self,request):
        pk=request.query_params.get('id')
        
        if not pk:
            return Response({"error": "Customer Id  is required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            customer=Customer.objects.get(pk=pk)
        
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
                
        data = {
            'first_name': request.query_params.get('first_name', customer.first_name),
            'last_name': request.query_params.get('last_name', customer.last_name),
            'phone_name': request.query_params.get('phone_name', customer.phone_name),
            'email': request.query_params.get('email', customer.email),
        }
        
        serializer = CustomerSerializer(customer, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class DeleteOneCustomerApi(APIView):
    
    def delete(self,request):
        pk=request.query_params.get('id')
        
        if not pk:
            return Response({"error": "Customer Id  is required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            customer=Customer.objects.get(pk=pk)
        
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND) 
       
        customer.delete()    
        return Response({"message": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)   
