from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import formset_factory
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime, timezone, timedelta
import hashlib

from .ImportFileManagement import FileImporter
from .models import FileImport_FileData, FileImport_AccountData, Accounts
from .transactionImportForms import TransactionFileUploadForm, ImportConfirmationForm

#--------------------------------------------------------------------------------------#
@login_required
def uploadTransactionFile(request):
    if request.method == 'POST':
        form = TransactionFileUploadForm(request.POST, request.FILES)
        if(form.is_valid()):

            #First thing is to store a record of the file in the database
            file = request.FILES['importFile']
            filename = file.name

            fileImporter = FileImporter(filename, file)
            fileImporter.importFile()

            accountModels = fileImporter.fileData.accounts
            if(accountModels.count() > 1):
                raise Exception("Each file should only contain one account for now.")

            importedAccount = accountModels.first()

            renderContext = {
                'account_id': importedAccount.account_id,
                'institution_name': importedAccount.institution_name,
                'modelMatched': importedAccount.matched,
            }

            # If the import matches an existing account. We should show it.
            if(importedAccount.matched):
                existingAccount = importedAccount.matched_account_id
                renderContext['existing_account_name'] = existingAccount.name
                renderContext['existing_account_institution'] = existingAccount.institution_name
                renderContext['existing_account_id'] = existingAccount.account_id
                return render(request, 'main/importsuccessful.html', renderContext)
            #otherwise we need to present a list of accounts to match it to.
            else:
                renderContext['form'] = ImportConfirmationForm({'fileHash': fileImporter.fileHash})
                #renderContext['form'].fileHash.initial = fileImporter.fileHash
                return render(request,'main/importconfirmation.html', renderContext)

        else:
            print("Invalid form")
            print(form.errors)


    else:
        form = TransactionFileUploadForm()
        return render(request, 'main/uploadTransactionFile.html', { 'form': form })

#---------------------------------------------------------------------------------------------------#
@login_required
def confirmUpload(request):

    if request.method == 'POST':
        form = ImportConfirmationForm(request.POST)
        if(form.is_valid()):
            fileHash = form.cleaned_data['fileHash']
            Account = form.cleaned_data['Account']

            if(Account == None):
                #This must be a new account
                FileImport_FileData.saveNewFile(fileHash)
            else:
                raise NotImplementedError("We don't support selecting unmatched files quite yet.")
        else:
            print("Invalid Form")
            print(form.errors)
            raise Exception("Invalid import cofirmation form recieved.")

    return HttpResponse("I'm not saving it yet because i'm not programmed to. but here I am. Come and fix me")
