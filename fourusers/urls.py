from django.urls import path
from . import views

app_name = 'fourusers'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('profile/<int:pk>', views.ProfilePage.as_view(), name='profile'),
    path('settings/', views.settings, name='settings'),
]