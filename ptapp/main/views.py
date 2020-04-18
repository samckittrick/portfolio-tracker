from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    context = { 'text': "Hello, this is the droid you are looking for" }
    return render(request, 'main/index.html', context)
