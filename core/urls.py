from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('employer/signup/', views.employer_signup, name='employer_signup'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
]