from rest_framework import generics
from manager.serializers import BalanceSerializer, BalanceAdminSerializer, TransactionUserSerializer, \
                                ListTransactionsSerializer, TransactionCategorySerializer
# from manager.serializers import CatatSerializer
from rest_framework.response import Response
from manager.models import Balance, Transaction
from manager.permissions import IsOwner
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User
from manager.pagination import ListPagination
# from manager.models import Catat


class ListCreateBalanceAPIView(generics.ListCreateAPIView):

    serializer_class = BalanceSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return Balance.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        Balance.objects.filter(user=request.user).delete()

        return self.create(request, *args, **kwargs)


class ListBalanceAdminAPIView(generics.ListAPIView):

    queryset = Balance.objects.all()
    serializer_class = BalanceAdminSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = ListPagination


class ListTransactionsAPIView(generics.ListAPIView):

    queryset = Transaction.objects.all()
    serializer_class = ListTransactionsSerializer
    pagination_class = ListPagination


class TransactionsCategoryAPIView(generics.ListCreateAPIView):

    queryset = Transaction.objects.filter(to_user__exact='')
    serializer_class = TransactionCategorySerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ListPagination

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


class TransactionsUserAPIView(generics.ListCreateAPIView):

    queryset = Transaction.objects.filter(category__exact='', organization__exact='')
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




#
# class CatatAPIView(generics.ListCreateAPIView):
#     queryset = Catat.objects.all()
#     serializer_class = CatatSerializer