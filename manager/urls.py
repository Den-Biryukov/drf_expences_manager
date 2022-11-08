from django.urls import path
from manager.views import ListAllBalancesForAdminAPIView, ListAllTransactionsForAdminAPIView, \
                          ListTransactionAPIView, TransactionCategoryAPIView, TransactionUserAPIView, \
                          ListCreateBalanceAPIView, ListUserStatisticAPIView,\
                          ListCreateCategoryAPIView, UpdateDestroyCategoryAPIView


# Admin
urlpatterns = [
    path('balance-admin/', ListAllBalancesForAdminAPIView.as_view()),
    path('transaction-admin/', ListAllTransactionsForAdminAPIView.as_view()),
]

# Transactions
urlpatterns += [
    path('transaction/', ListTransactionAPIView.as_view()),
    path('transaction/category/', TransactionCategoryAPIView.as_view()),
    path('transaction/to_user/', TransactionUserAPIView.as_view()),
]

# User
urlpatterns += [
    path('balance/', ListCreateBalanceAPIView.as_view()),
    path('statistic/', ListUserStatisticAPIView.as_view()),
    path('category/', ListCreateCategoryAPIView.as_view()),
    path('category/<int:pk>/', UpdateDestroyCategoryAPIView.as_view()),
]
