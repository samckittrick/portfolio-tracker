from django.contrib import admin

from .models import FileImport_FileData, FileImport_AccountData

# Register your models here.
#Remove later because this doesn't need to be managed through the account
admin.site.register(FileImport_FileData)
admin.site.register(FileImport_AccountData)
