from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Accounts
from .types import AccountTypes
from .FinanceAnalysis import getNetWorth

# Create your views here.
@login_required
def index(request):
    """Generates the home dashboard"""
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

@login_required
def accountListing(request):
    """Generate page for listing accounts and their transactions"""

    #For now all the account data gets sent. Eventually, this should
    # be broken up with ajax to reduce the amount sent at one time
    account_list_display = list()
    accountlist = Accounts.objects.filter(accountActive = True)
    for a in accountlist:
        accountDict = {
            'name': a.name,
            'value': a.getValue(),
            'type': a.type,
        }

        if(a.type == AccountTypes.BANK_TYPE):
            accountDict['transactions'] = list()
            for t in a.getSubclass().transactions.all():
                tdata = {
                    'date': t.date,
                    'amount': t.amount,
                    'memo': t.memo
                }
                accountDict['transactions'].append(tdata)
        elif(a.type == AccountTypes.INVESTMENT_TYPE):
            accountDict['positions'] = list()
            for p in a.getSubclass().positions.all():
                pdata = {
                    'ticker': p.ticker,
                    'units': p.units,
                    'unit_price': p.unit_price
                }
                accountDict['positions'].append(pdata)

            accountDict['transactions'] = list()
            for t in a.getSubclass().transactions.all():
                tdata = {
                    'date': t.settleDate,
                    'amount': t.total,
                    'memo': t.memo
                }
                accountDict['transactions'].append(tdata)

        account_list_display.append(accountDict)

    context = {
        'accountlist': account_list_display
    }

    return render(request, 'main/accountlist.html', context)
