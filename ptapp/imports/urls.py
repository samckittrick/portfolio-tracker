from django.urls import path

from . import views

app_name = 'imports'
urlpatterns = [
    path('upload/', views.uploadTransactionFile, name='uploadTransactionFile'),
    path('confirmupload', views.confirmUpload, name='confirmupload')
]
