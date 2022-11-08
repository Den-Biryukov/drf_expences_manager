from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Max, Min, Avg
from django.db.models.functions import Round
from manager.models import Balance, Category, Transaction
from manager.serializers import CategorySerializer, BalanceSerializer, \
                                ListTransactionSerializer, BalanceAdminSerializer, TransactionAdminSerializer, \
                                TransactionCategoryListSerializer, TransactionUserSerializer, \
                                TransactionCategoryPostSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from manager.permissions import IsOwner
from manager.pagination import ListPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.contrib.auth.models import User


class ListUserStatisticAPIView(APIView):
    """Show some user statistic"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(
            {'total transactions': Transaction.objects.filter(owner=request.user).count(),
             'max sum of transaction':
                 Transaction.objects.filter(owner=request.user).
                 aggregate(res=Max('sum_of_transaction'))['res'],
             'min sum of transaction':
                 Transaction.objects.filter(owner=request.user).
                 aggregate(res=Min('sum_of_transaction'))['res'],
             'avg sum of transaction':
                 Transaction.objects.filter(owner=request.user).
                 aggregate(res=Round(Avg('sum_of_transaction'), 2))['res']
             }
        )


class ListCreateCategoryAPIView(generics.ListCreateAPIView):
    """Show user categories. Create custom categories"""

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class UpdateDestroyCategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Update and delete user categories"""

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)


class ListCreateBalanceAPIView(generics.ListCreateAPIView):
    """Get and replenishment user amount"""

    serializer_class = BalanceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Balance.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        Balance.objects.filter(user=request.user).delete()
        return self.create(request, *args, **kwargs)


class ListTransactionAPIView(generics.ListAPIView):
    """Show user transactions"""

    queryset = Transaction.objects.all()
    serializer_class = ListTransactionSerializer
    pagination_class = ListPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['category', 'sum_of_transaction', 'organization']
    ordering_fields = ['category', 'sum_of_transaction', 'time_of_transaction', 'organization']


class ListAllBalancesForAdminAPIView(generics.ListAPIView):
    """Show balance of each user for admin"""

    queryset = Balance.objects.all()
    serializer_class = BalanceAdminSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = ListPagination


class ListAllTransactionsForAdminAPIView(generics.ListAPIView):
    """Show transaction of each user for admin"""

    queryset = Transaction.objects.all()
    serializer_class = TransactionAdminSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = ListPagination


class TransactionCategoryAPIView(generics.ListCreateAPIView):
    """Make a transaction by category"""

    queryset = Transaction.objects.filter(to_user__exact='')
    permission_classes = (IsAuthenticated,)
    pagination_class = ListPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TransactionCategoryListSerializer
        else:
            return TransactionCategoryPostSerializer

    def post(self, request, *args, **kwargs):

        sum_of_transaction = request.POST.get('sum_of_transaction')

        if sum_of_transaction.isalnum():
            if self.request.user.balances.amount - int(sum_of_transaction) < 0:
                return Response(
                    f"You haven't enough money. You have "
                    f"{self.request.user.balances.amount} c.u., but you need {sum_of_transaction} c.u."
                )
            else:
                self.request.user.balances.amount -= int(sum_of_transaction)
                self.request.user.balances.save()
                return self.create(request, *args, **kwargs)
        else:
            return Response('Enter numbers')


class TransactionUserAPIView(generics.ListCreateAPIView):
    """Make a transaction per suer"""

    queryset = Transaction.objects.filter(organization__exact=None)
    serializer_class = TransactionUserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ListPagination

    def post(self, request, *args, **kwargs):

        sum_of_transaction = request.POST.get('sum_of_transaction')
        to_user = User.objects.get(username=request.POST.get('to_user'))

        if sum_of_transaction.isalnum():
            if self.request.user.balances.amount - int(sum_of_transaction) < 0:
                return Response(
                    f"You haven't enough money. You have "
                    f"{self.request.user.balances.amount} c.u., but you need {sum_of_transaction} c.u."
                )
            else:
                self.request.user.balances.amount -= int(sum_of_transaction)
                to_user.balances.amount += int(sum_of_transaction)
                self.request.user.balances.save()
                to_user.balances.save()
                return self.create(request, *args, **kwargs)
        else:
            return Response('Enter numbers')
