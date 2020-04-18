from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Accounts
# Create your views here.
@login_required
def index(request):
    accountlist = Accounts.objects.all()
    context = {
        'accountlist': accountlist
    }
    return render(request, 'main/index.html', context)
