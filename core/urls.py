from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as core_views

app_name = 'core'
urlpatterns = [
    path('', core_views.home, name='home'),
    
    # employer only
    path('employer/signup/', core_views.employer_signup, name='employer_signup'),
    path('employer/dashboard/', core_views.employer_dashboard, name='employer_dashboard'),
    path('employer/employees/', core_views.employees_list, name='employees_list'),
    
    # employee only
    path('employee/dashboard/', core_views.employee_dashboard, name='employee_dashboard'),
    
    # all users
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login_redirect', core_views.login_redirect, name='login_redirect'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]