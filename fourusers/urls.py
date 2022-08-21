from django.urls import path
from . import views

app_name = 'fourusers'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.view_user, name='user'),
    path('user/settings/', views.settings, name='settings'),
]