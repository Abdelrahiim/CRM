from django.urls import path
from team.views import EditTeam,TeamDetails

app_name = 'team'
urlpatterns = [
    path('<str:pk>/edit/',EditTeam.as_view(),name='edit'),
    path('<str:pk>/',TeamDetails.as_view(),name='detail')
]
