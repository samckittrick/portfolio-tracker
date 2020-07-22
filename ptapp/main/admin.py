from django.contrib import admin
from .models import Accounts, AccountAliases, CashAccounts, CashTransaction, InvestmentAccounts, InvestmentPosition, InvestmentTransaction

# Register your models here.
class AccountAliasInLine(admin.StackedInline):
    model = AccountAliases
    extra = 1

class AccountsAdmin(admin.ModelAdmin):
    inlines = [AccountAliasInLine]

admin.site.register(Accounts, AccountsAdmin)
admin.site.register(CashTransaction)
admin.site.register(CashAccounts)
admin.site.register(InvestmentAccounts)
admin.site.register(InvestmentPosition)
admin.site.register(InvestmentTransaction)
