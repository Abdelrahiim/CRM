from django.urls import path
from team.views import EditTeam

app_name = 'team'
urlpatterns = [
    path('<str:pk>/edit/',EditTeam.as_view(),name='edit')
]
