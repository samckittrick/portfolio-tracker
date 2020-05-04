from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import formset_factory
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime, timezone, timedelta
import hashlib

from .ImportFileManagement import FileImporter
from main.models import Accounts
from .models import FileData, AccountData
from .forms import TransactionFileUploadForm, ImportConfirmationForm
from .exceptions import FileImportException

#--------------------------------------------------------------------------------------#
def renderErrorPage(request, errorText):
    """
    Renders and returns an error page to be displayed to the user

    @param request: django.http.HTTPRequest - The context of the http request
    @param errorText: string - The text of the error to display
    """
    return render(request, 'imports/importerror.html', { 'errorText': errorText } )

#--------------------------------------------------------------------------------------#
def renderConfirmationPage(request, fileImporter):
    """
    Renders the confirmation page for a given import

    @param request: django.http.HTTPRequest - The context of the http request
    @param fileImporter: .ImportFileManagement.FileImporter - The importer object that contains the data
    """

    accountModels = fileImporter.fileData.accounts

    # This is the data that will be passed to the template
    renderContext = {
        'accounts': list()
    }

    # This is the initial data for creating the formset.
    formsetInitialData = list()

    for account in accountModels.all():
        renderAccount = {
            'account_id': account.account_id,
            'institution_name': account.institution_name,
            'accountMatched': account.matched
        }

        # If the import matches an existing account. We should show it.
        if(account.matched):
            existingAccount = account.matched_account_id
            renderAccount['existing_account_name'] = existingAccount.name
            renderAccount['existing_account_id'] = existingAccount.account_id
            renderAccount['existing_account_institution'] = existingAccount.institution_name
        # If we didn't make the match, then we should give a form to select an account
        else:
            formsetInitialData.append({
            'fileHash': fileImporter.fileHash,
            'accountId': account.account_id
            })

        renderContext['accounts'].append(renderAccount)

    # Since we can have multiple unmatched accounts, we have to create a formset
    #   of forms for manually selecting a match.
    # Because its possible to have a mix of matched and unmatched accounts, we
    #   need to display the forms separately and match them with the associated data
    #   in the renderContext account list.

    ImportConfirmationFormset = formset_factory(ImportConfirmationForm, extra=0)
    formset = ImportConfirmationFormset(initial= formsetInitialData)

    # Formsets have extra fields for managing them. We will display them separately
    renderContext['formsetManager'] = formset.management_form

    # Match up entries in the formset to entries in the accounts list
    for f in formset.forms:
        for a in renderContext['accounts']:
            if(f['accountId'].value() == a['account_id']):
                a['selectForm'] = f

    return render(request,'imports/importconfirmation.html', renderContext)

#--------------------------------------------------------------------------------------#
@login_required
def uploadTransactionFile(request):
    """
    Present the form for uploading a file with transaction information, parse it and respond
    """
    if request.method == 'POST':
        form = TransactionFileUploadForm(request.POST, request.FILES)
        if(form.is_valid()):

            #First thing is to store a record of the file in the database
            file = request.FILES['importFile']
            filename = file.name

            try:
                fileImporter = FileImporter(filename, file)
                fileImporter.importFile()
            except FileImportException as e:
                return renderErrorPage(request, str(e))

            return renderConfirmationPage(request, fileImporter)

        else:
            print("Invalid form")
            print(form.errors)


    else:
        form = TransactionFileUploadForm()
        return render(request, 'imports/uploadTransactionFile.html', { 'form': form })

#---------------------------------------------------------------------------------------------------#
@login_required
def confirmUpload(request):
    """
    Receive the match confirmation form and save the data into the database
    """
    if request.method == 'POST':
        ImportConfirmationFormset = formset_factory(ImportConfirmationForm, extra=0)
        formset = ImportConfirmationFormset(request.POST)
        if(formset.is_valid()):
            fileHashList = list()

            # For each unmatched item in the temporary database, update the match
            for form in formset:
                fileHash = form.cleaned_data['fileHash']
                if(fileHash not in fileHashList):
                    fileHashList.append(fileHash)

                account_id = form.cleaned_data['accountId']
                Account = form.cleaned_data['Account']

                dbEntry = FileData.objects.get(pk=fileHash).accounts.get(account_id=account_id)
                if(Account is not None):
                    dbEntry.matched_account_id = Account
                    dbEntry.matched = True

                dbEntry.save()

            # For each file that is being confirmed.
            for h in fileHashList:
                fileEntry = FileData.objects.get(pk=fileHash)
                fileEntry.completeImportFile()
                fileEntry.delete()

            return render(request, 'imports/importsuccessful.html')

        else:
            print(form.errors)
            return renderErrorPage(request, "Invalid confirmation form")

    # If the methood is not POST, then something went wrong:
    else:
        return renderErrorPage(request, "You must have accessed this page directly. This page is only for confirming file uploads")
