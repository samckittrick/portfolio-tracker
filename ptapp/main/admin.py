from django.contrib import admin
from .models import Accounts, AccountAliases

# Register your models here.
class AccountAliasInLine(admin.StackedInline):
    model = AccountAliases
    extra = 1

class AccountsAdmin(admin.ModelAdmin):
    inlines = [AccountAliasInLine]

admin.site.register(Accounts, AccountsAdmin)
