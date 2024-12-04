from django.db import models

# Create your models here.
class Customer (models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    phone_name=models.CharField(max_length=20)
    email=models.EmailField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name},{self.phone_name},{self.email}"