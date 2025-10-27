from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view,name="login"),
    path('register/', views.register,name="register"),
    path('logout/', views.logout_view,name="logout"),

    path('user_dashboard/', views.user_dashboard,name="user_dashboard"),
    path('admin_dashboard/', views.admin_dashboard,name="admin_dashboard"),

    path('complaint_registration_form/', views.complaint_registration_form,name="complaint_registration_form"),
    path('all_complaints/', views.all_complaints,name="all_complaints"),
    path('submitted_complaints/', views.submitted_complaints,name="submitted_complaints"),
    path('update_complaint/<int:id>/', views.update_complaint,name="update_complaint"),
    path('success/', views.success,name="success"),

    path('forgot_password/', views.forgot_password,name="forgot_password"),
    path('reset_password/<str:email>/', views.reset_password,name="reset_password"),
]