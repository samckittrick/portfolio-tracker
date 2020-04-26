from django.contrib import admin

from .models import FileData, AccountData

# Register your models here.
#Remove later because this doesn't need to be managed through the account
admin.site.register(FileData)
admin.site.register(AccountData)
