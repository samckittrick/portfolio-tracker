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
    for a in accountlist:
        networth_breakdown_list['labels'].append(a.name)
        networth_breakdown_list['data'].append(a.balance)

    context = {
        'accountlist': accountlist,
        'netWorth': netWorth,
        'networth_breakdown_list': networth_breakdown_list
    }
    return render(request, 'main/index.html', context)
