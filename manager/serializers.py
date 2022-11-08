from rest_framework import serializers
from .models import Balance, Category, Transaction


class CategorySerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = '__all__'


class BalanceSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Balance
        fields = ('user', 'amount')


class ListTransactionSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_category_name(self, obj):
        if hasattr(obj.category, 'name'):
            return obj.category.name
        else:
            return 'transaction to user'

    category = serializers.SerializerMethodField('get_category_name')

    class Meta:
        model = Transaction
        exclude = ('id',)
        depth = 1


class BalanceAdminSerializer(serializers.ModelSerializer):

    def get_user_id_and_username(self, obj):
        return {'id': obj.user.id, 'username': obj.user.username}

    user = serializers.SerializerMethodField('get_user_id_and_username')

    class Meta:
        model = Balance
        fields = '__all__'


class TransactionAdminSerializer(serializers.ModelSerializer):

    def get_user_id_and_username(self, obj):
        return {'id': obj.user.id, 'username': obj.user.username}

    user = serializers.SerializerMethodField('get_user_id_and_username')

    class Meta:
        model = Balance
        fields = '__all__'


class TransactionCategoryListSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_category_name(self, obj):
        return obj.category.name

    category = serializers.SerializerMethodField('get_category_name')

    class Meta:
        model = Transaction
        exclude = ('id', 'to_user')


class TransactionCategoryPostSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Transaction
        exclude = ('id', 'to_user')


class TransactionUserSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Transaction
        fields = ('to_user', 'time_of_transaction', 'sum_of_transaction', 'owner')
