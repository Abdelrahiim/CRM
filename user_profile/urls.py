from django.urls import path
from django.contrib.auth import views
from .views import SignInView
views.LogoutView
urlpatterns = [
    path('sign-in/',SignInView.as_view(),name='signup'),
    path('log-in/',views.LoginView.as_view(template_name = "user_profile/sign_in.html"),name= 'login'),
    path('log-out/',views.LogoutView.as_view(),name= 'logout')
    
]
