from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from Hospital import views
from medcare import settings

app_name = 'Hospital'

urlpatterns = [
    path(r'', views.login, name='login'),
    path(r'location/<string>/', views.location, name="location"),
    path(r'dashboard/', views.dashboard, name='dashboard'),
    path(r'Hospital/', views.list_hospital, name='list_hospital'),
    path(r'Register/', views.register, name='register'),
    path(r'excel/<string>/', views.excel, name='excel'),
    path(r'appointment/<string>/', views.appointment, name='appointment'),
    path(r'symptomChecker/', views.symp_checker , name='symptom_checker'),
    path(r'order_medicine/', views.order_medicine, name='order'),
]
