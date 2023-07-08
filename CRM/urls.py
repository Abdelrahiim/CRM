
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('core.urls')),
    path('',include('user_profile.urls')),
    path('dashboard/',include('dashboard.urls')),
    path("dashboard/team/", include('team.urls')),
    path('leads/',include('leads.urls')),
    path('clients/',include('client.urls')),
    
]
