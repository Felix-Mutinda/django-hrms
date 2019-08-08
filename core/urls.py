from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as core_views

app_name = 'core'
urlpatterns = [
    path('', core_views.home, name='home'),
    path('employer/signup/', core_views.employer_signup, name='employer_signup'),
    path('employer/dashboard/', core_views.employer_dashboard, name='employer_dashboard'),
    path('employee/dashboard/', core_views.employee_dashboard, name='employee_dashboard'),
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login_redirect', core_views.login_redirect, name='login_redirect'),
]