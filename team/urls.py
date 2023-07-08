from django.urls import path
from team.views import EditTeam
urlpatterns = [
    path('<str:pk>/edit/',EditTeam.as_view(),name='edit-team')
]
