"""fourjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'fourjango'

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('fourapp.urls')), #incluyo las urls de fourapp para manejar todo desde la app en lugar de usar el root
    path('users/', include('fourusers.urls')), #incluyo las urls de fourusers para manejar todo desde la app en lugar de usar el root
    path('users/', include('django.contrib.auth.urls')), #incluyo las urls de django para manejar todo desde la app en lugar de usar el root

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #esto lo saqué de un video de codemy
