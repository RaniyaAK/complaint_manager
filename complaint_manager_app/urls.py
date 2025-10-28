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
    path('submitted_complaints/', views.submitted_complaints,name="submitted_complaints"),
    path('success/', views.success,name="success"),
    path('update_status/<int:complaint_id>/', views.update_status, name='update_status'),

    path('all_complaints/', views.all_complaints,name="all_complaints"),
    path('complaints_list/', views.complaints_list,name="complaints_list"),


    path('forgot_password/', views.forgot_password,name="forgot_password"),
    path('reset_password/<str:email>/', views.reset_password,name="reset_password"),
]