from django.urls import path
from django.contrib.auth import views
from user_profile.views import SignUpView , MyAccountView
from user_profile.forms import LoginForm

urlpatterns = [
    path('sign-up/',SignUpView.as_view(),name='signup'),
    path('log-in/',views.LoginView.as_view(template_name = "user_profile/sign_in.html",authentication_form = LoginForm),name= 'login'),
    path('log-out/',views.LogoutView.as_view(),name= 'logout'),
    path('dashboard/my-account/',MyAccountView.as_view(),name="my-account")
]
