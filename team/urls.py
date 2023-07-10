from django.urls import path
from team.views import EditTeam,TeamDetails,TeamList

app_name = 'team'
urlpatterns = [
    path('',TeamList.as_view(),name='list'),
    path('<str:pk>/edit/',EditTeam.as_view(),name='edit'),
    path('<str:pk>/',TeamDetails.as_view(),name='details')
]
