from django.urls import path
from . import views 

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('', views.dashboard, name='dashboardd'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('forget_password/', views.forget_password, name="forget_password"),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('reset_password/', views.reset_password, name="reset_password"),
]
