from itertools import product
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from product_catalog.models import Product
from product_catalog.serializer import ProductSerializer
# Create your views here.

class CreateProductApi(APIView):
    
    def post(self,request):
         serializer=ProductSerializer(data=request.data)
         if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Product CREATED'},status=status.HTTP_201_CREATED)    
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GetProductApi(APIView):
   
   def get(self,request):
        
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)
     
class GetOneProductApi(APIView):
    
    def get(self,request):
        product_name=request.query_params.get('product_name')
        
        if not product_name:
            return Response({"error": "product_name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product=Product.objects.get(product_name=product_name)
            
        except Product.DoesNotExist :
             return Response({"error": "product not found"}, status=status.HTTP_404_NOT_FOUND)  
         
        serializer=ProductSerializer(product)
        return Response(serializer.data)      
     
class UpdateOneProductApi(APIView):
    
    def put(self,request):
        pk=request.query_params.get('id')
        
        if not pk:
            return Response({"error": "Product Id  is required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product=Product.objects.get(pk=pk)
        
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
                
        data = {
            'product_type': request.query_params.get('product_type', product.product_type),
            'product_name': request.query_params.get('product_name', product.product_name),
            'description': request.query_params.get('description', product.description),
        }

        
        serializer = ProductSerializer(product, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class DeleteOneProductApi(APIView):
    
    def delete(self,request):
        pk=request.query_params.get('id')
        
        if not pk:
            return Response({"error": "Product Id  is required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product=Product.objects.get(pk=pk)
        
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND) 
         
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    