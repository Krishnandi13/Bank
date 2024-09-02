from django.urls import path
from product_catalog.views import CreateProductApi,GetProductApi,GetOneProductApi,UpdateOneProductApi,DeleteOneProductApi

urlpatterns = [
    path('create/',CreateProductApi.as_view()),
    path('fetch/',GetProductApi.as_view()),
    path('fetch-one/',GetOneProductApi.as_view()),
    path('update-one/',UpdateOneProductApi.as_view()),
    path('delete-one/',DeleteOneProductApi.as_view()),
    
    
]


