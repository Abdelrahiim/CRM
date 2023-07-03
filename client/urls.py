from django.urls import path
from client.views import ClientList

urlpatterns = [
    path('',ClientList.as_view(),name='clients')
]
