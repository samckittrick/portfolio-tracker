from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Accounts
from .FinanceAnalysis import getNetWorth

# Create your views here.
@login_required
def index(request):
    accountlist = Accounts.objects.filter(accountActive = True)
    netWorth = getNetWorth()

    # Build out the structure needed for the networth breakdown chart
    networth_breakdown_list = { 'labels': list(), 'data': list() }
    # Build out the structure needed for the table of accounts
    account_list_display = list()
    for a in accountlist:
        name = a.name
        value = a.getValue()

        account_list_display.append({'name': name, 'balance': value})
        networth_breakdown_list['labels'].append(name)
        networth_breakdown_list['data'].append(value)

    context = {
        'accountlist': account_list_display,
        'netWorth': netWorth,
        'networth_breakdown_list': networth_breakdown_list
    }
    return render(request, 'main/index.html', context)
