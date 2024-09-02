from django.urls import path
from account.views import CreateAccountApi,GetAllAccounts,GetOneAccount,CloseAccountApi,DepositApi,WithdrawApi,TransactionStatement

urlpatterns = [
    path('create/',CreateAccountApi.as_view()),
    path('fetch/',GetAllAccounts.as_view()),
    path('fetch-One/',GetOneAccount.as_view()),
    path('close/',CloseAccountApi.as_view()),
    path('deposit/',DepositApi.as_view()),
    path('withdraw/',WithdrawApi.as_view()),
    path('transaction/',TransactionStatement.as_view()),
]