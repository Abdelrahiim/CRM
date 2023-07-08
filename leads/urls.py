from django.urls import path

from leads.views import AddLeadView, ListAllLeads, DeleteLead, SingleLead, UpdateLead , ConvertToClient

app_name = 'leads'

urlpatterns = [
    path('create/', AddLeadView.as_view(), name='create'),
    path('', ListAllLeads.as_view(), name='list'),
    path("<str:pk>/", SingleLead.as_view(), name='details'),
    path("update/<str:pk>", UpdateLead.as_view(), name='edit'),
    path('delete/<str:pk>/', DeleteLead.as_view(), name='delete'),
    path('convert/<str:pk>/', ConvertToClient.as_view(), name='convert')
]
