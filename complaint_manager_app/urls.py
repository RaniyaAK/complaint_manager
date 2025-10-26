from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login,name="login"),
    path('register/', views.register,name="register"),
    path('user_dashboard/', views.user_dashboard,name="user_dashboard"),
    path('admin_dashboard/', views.admin_dashboard,name="admin_dashboard"),
    # path('complaint_registration_form/', views.complaint_registration_form,name="complaint_registration_form"),
]