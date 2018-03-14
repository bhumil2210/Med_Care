from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from Hospital import views
from medcare import settings

app_name = 'Hospital'

urlpatterns = [
    path(r'', views.login, name='login'),
    path(r'dashboard/', views.dashboard, name='dashboard'),
    path(r'Hospital/', views.list_hospital, name='list_hospital'),
    path(r'Register/', views.register, name='register'),
    path(r'excel/', views.excel, name='excel'),
    path(r'appointment/<string>/', views.appointment, name='appointment')
]
