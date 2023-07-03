from django.urls import path

from leads.views import AddLeadView, ListAllLeads, DeleteLead, SingleLead, UpdateLead , ConvertToClient

urlpatterns = [
    path('create/', AddLeadView.as_view(), name='leads'),
    path('', ListAllLeads.as_view(), name='leads_list'),
    path("<str:pk>/", SingleLead.as_view(), name='single_lead'),
    path("update/<str:pk>", UpdateLead.as_view(), name='leads_edit'),
    path('delete/<str:pk>/', DeleteLead.as_view(), name='leads_delete'),
    path('convert/<str:pk>/', ConvertToClient.as_view(), name='convert_lead')
]
