from django.contrib import admin
from .models import Balance, Transaction, Category


admin.site.register(Balance)
admin.site.register(Transaction)
admin.site.register(Category)
