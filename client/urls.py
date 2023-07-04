from django.urls import path
from client.views import ClientList,SingleClient,CreateNewCLient,DeleteClient,UpdateClient

urlpatterns = [
    path('',ClientList.as_view(),name='clients'),
    path('create/',CreateNewCLient.as_view(),name='create-client'),
    path('<str:pk>/', SingleClient.as_view(),name='single-client'),
    path('<str:pk>/update', UpdateClient.as_view(),name='edit-client'),
    path('<str:pk>/delete', DeleteClient.as_view(),name='remove-client'),
]
