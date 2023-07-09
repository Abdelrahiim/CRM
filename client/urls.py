from django.urls import path
from client.views import ClientList,UploadFileView,SingleClient,CreateNewClient,DeleteClient,UpdateClient

app_name = 'client'

urlpatterns = [
    path('',ClientList.as_view(),name='list'),
    path('create/',CreateNewClient.as_view(),name='create'),
    path('<str:pk>/', SingleClient.as_view(),name='details'),
    path('<str:pk>/update', UpdateClient.as_view(),name='edit'),
    path('<str:pk>/delete', DeleteClient.as_view(),name='remove'),
    path('<str:pk>/add-file',UploadFileView.as_view(),name='add-file')
]
