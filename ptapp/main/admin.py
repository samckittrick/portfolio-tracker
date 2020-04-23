from django.contrib import admin
from .models import Accounts, AccountAliases, FileImport_FileData, FileImport_AccountData

# Register your models here.
class AccountAliasInLine(admin.StackedInline):
    model = AccountAliases
    extra = 1

class AccountsAdmin(admin.ModelAdmin):
    inlines = [AccountAliasInLine]

admin.site.register(Accounts, AccountsAdmin)

#Remove later because this doesn't need to be managed through the account
admin.site.register(FileImport_FileData)
admin.site.register(FileImport_AccountData)
