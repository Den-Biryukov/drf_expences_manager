from django.contrib import admin
from .models import Balance, Transaction, Category


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'sum_of_transaction', 'time_of_transaction', 'category',
                    'to_user', 'organization', 'description')
    list_filter = ('owner', 'to_user')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')
    list_filter = ('user', 'name')


admin.site.register(Balance)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category, CategoryAdmin)
