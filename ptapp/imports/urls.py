from django.urls import path

from . import views
from . import transactionImportViews

app_name = 'imports'
urlpatterns = [
    path('upload/', transactionImportViews.uploadTransactionFile, name='uploadTransactionFile'),
    path('confirmupload', transactionImportViews.confirmUpload, name='confirmupload')
]
