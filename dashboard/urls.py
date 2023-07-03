from django.urls import path
from .views import DashBoard

urlpatterns = [
    
    path('',DashBoard.as_view(),name='dashboard')
]