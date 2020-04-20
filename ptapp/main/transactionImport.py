from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

from .ImportFileManagement import OFXFile
from .models import FileImportAccountData, Accounts

###################################################
# Class representing the form used for uploading
# lists of transactions for analysis
###################################################
class TransactionFileUploadForm(forms.Form):
    importFile = forms.FileField()

@login_required
def uploadTransactionFile(request):
    if request.method == 'POST':
        form = TransactionFileUploadForm(request.POST, request.FILES)
        if(form.is_valid()):
            filename = request.FILES['importFile'].name
            if(filename.lower().endswith("qfx") or filename.lower().endswith("ofx")):
                importedFile = OFXFile(fileobj = request.FILES['importFile'])

                for account in importedFile.parsedData:
                    model = FileImportAccountData()
                    model.account_id = account['account_id']
                    model.routing_number = account['routing_number']
                    model.institution_name = account['institution_name']
                    model.institution_id = account['institution_id']
                    model.currency_symbol = account['currency_symbol']
                    model.balance = 0.00
                    model.balance_date = datetime.now()

                    #Match it with an existing account
                    existingAccountsModel = Accounts.objects
                    try:
                        existingAccount = existingAccountsModel.get(account_id = model.account_id, institution_id = model.institution_id)
                        model.matched = True
                        model.matched_account_id = existingAccount
                    except ObjectDoesNotExist:
                        model.matched = False

                    model.save()

                    print(model.id)
                    renderContext = {
                        'id': model.id,
                        'account_id': model.account_id,
                        'institution_name': model.institution_name,
                        'modelMatched': model.matched
                    }

                    if(model.matched):
                        renderContext['existing_account'] = existingAccount.name
                        
                    return render(request,'main/importconfirmation.html', renderContext)
        else:
            print("Invalid form")
            print(form.errors)

        return HttpResponse("<a href=\"/admin/\">Whaaa???</a>")

    else:
        form = TransactionFileUploadForm()
        return render(request, 'main/uploadTransactionFile.html', { 'form': form })
