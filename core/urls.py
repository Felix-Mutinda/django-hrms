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
    path('employer/assets/', core_views.employer_assets, name='employer_assets'),
    path('employer/notifications/', core_views.employer_notifications, name='employer_notifications'),
    path('employer/profile/', core_views.employer_profile, name='employer_profile'),
    path('employee/add/', core_views.employee_add, name='employee_add'),
    path('asset/add/', core_views.asset_add, name='asset_add'),
    
    # employee only
    path('employee/dashboard/', core_views.employee_dashboard, name='employee_dashboard'),
    
    # all users
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login_redirect', core_views.login_redirect, name='login_redirect'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]