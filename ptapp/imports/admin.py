from django.contrib import admin

from .models import FileData, AccountData, CashAccountData, CashTransaction, InvestmentAccountData, InvestmentPosition, InvestmentTransaction

# Register your models here.
#Remove later because this doesn't need to be managed through the account
admin.site.register(FileData)
admin.site.register(AccountData)
admin.site.register(CashAccountData)
admin.site.register(CashTransaction)
admin.site.register(InvestmentAccountData)
admin.site.register(InvestmentPosition)
admin.site.register(InvestmentTransaction)
