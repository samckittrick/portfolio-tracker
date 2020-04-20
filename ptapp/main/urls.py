from django.urls import path

from . import views
from . import transactionImport

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('import/upload/', transactionImport.uploadTransactionFile, name='uploadTransactionFile')
]
