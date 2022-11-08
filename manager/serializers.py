from rest_framework import serializers
from .models import Balance
from .models import Transaction
# from .models import Catat
# from .models import Replenishment


class BalanceSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Balance
        fields = ('user', 'amount')


class BalanceAdminSerializer(serializers.ModelSerializer):

    def get_id_and_username(self, obj):
        return {'id': obj.user.id, 'username': obj.user.username}

    user = serializers.SerializerMethodField('get_id_and_username')

    class Meta:
        model = Balance
        fields = '__all__'


# class ReplenishmentSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Replenishment
#         fields = '__all__'

#


class ListTransactionsSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

   #  def get_category_name(self, obj):
   #      return {'cat_name': obj.categories.name}
   #
   # category = serializers.SerializerMethodField('get_category_name')

    class Meta:
        model = Transaction
        exclude = ('id',)


class TransactionCategorySerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Transaction
        exclude = ('id', 'to_user')


class TransactionUserSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Transaction
        fields = ('to_user', 'time_of_transaction', 'sum_of_transaction', 'owner')







# class CatatSerializer(serializers.ModelSerializer):
#
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = Catat
#         fields = '__all__'