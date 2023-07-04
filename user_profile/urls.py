from django.urls import path
from django.contrib.auth import views
from user_profile.views import SignUpView



urlpatterns = [
    path('sign-up/',SignUpView.as_view(),name='signup'),
    path('log-in/',views.LoginView.as_view(template_name = "user_profile/sign_in.html"),name= 'login'),
    path('log-out/',views.LogoutView.as_view(),name= 'logout')
    
]
