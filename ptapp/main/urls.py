from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    #path('import/upload/', transactionImportViews.uploadTransactionFile, name='uploadTransactionFile'),
    #path('import/confirmupload', transactionImportViews.confirmUpload, name='confirmupload')
]
