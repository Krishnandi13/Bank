from rest_framework import serializers

from product_catalog.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['product_type','product_name','description']
        