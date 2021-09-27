"""Zavrsni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from SPA.views import  home_view, contact_view, map_view, taz_view, \
    taz_maker, ok_view, spremi_view
urlpatterns = [
    path('', home_view, name='home'),
    path('contact/', contact_view, name='contact'),
    path('karta/', map_view, name='map'),
    path('admin/', admin.site.urls),
    path('taz_solver/', taz_view, name='taz_solver'),
    path('taz_maker/', taz_maker, name='taz_maker'),
    path('spremi', spremi_view, name='spremi'),
    path('ok/', ok_view, name='ok'),


]
