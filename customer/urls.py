from django.urls import path
from customer.views import CreateCustomerAPI,GetAllCustomerApi,GetOneCustomerApi,UpdateOneCustomerApi,DeleteOneCustomerApi

urlpatterns = [
    path('create/',CreateCustomerAPI.as_view()),
    path('fetch/',GetAllCustomerApi.as_view()),
    path('fetch-one/',GetOneCustomerApi.as_view()),
    path('update-one/',UpdateOneCustomerApi.as_view()),
    path('delete-one/',DeleteOneCustomerApi.as_view()),
    
]
