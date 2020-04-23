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

            model = accountModels.first()
            
            renderContext = {
                'account_id': model.account_id,
                'institution_name': model.institution_name,
                'modelMatched': model.matched,
            }

            # If the import matches an existing account. We should show it.
            if(model.matched):
                renderContext['existing_account_name'] = existingAccount.name
                renderContext['existing_account_institution'] = existingAccount.institution_name
                renderContext['existing_account_id'] = existingAccount.account_id
            #otherwise we need to present a list of accounts to match it to.
            else:
                renderContext['form'] = ImportConfirmationForm()


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
    return HttpResponse("I'm not saving it yet because i'm not programmed to. but here I am. Come and fix me")
