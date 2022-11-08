from django.urls import path
from manager.views import ListCreateBalanceAPIView, ListBalanceAdminAPIView, \
                          ListTransactionsAPIView, TransactionsCategoryAPIView, \
                          TransactionsUserAPIView


urlpatterns = [
    path('balance/', ListCreateBalanceAPIView.as_view()),
    path('balance-admin/', ListBalanceAdminAPIView.as_view()),
]

# Transactions
urlpatterns += [
    path('transactions/', ListTransactionsAPIView.as_view()),
    path('transactions/category/', TransactionsCategoryAPIView.as_view()),
    path('transactions/user/', TransactionsUserAPIView.as_view()),
]
