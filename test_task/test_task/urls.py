"""
URL configuration for test_task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from tkinter.font import names

from django.contrib import admin
from django.urls import path

from weather import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', views.get_weather_by_coordinate, name = 'get_weather_by_coordinate'),
    path('weather_with_params/', views.get_weather_by_city_and_time, name = 'weather_with_params'),
    path('cities/', views.get_cities_list, name = 'cities'),
    path('additing_city/', views.add_city, name = 'additing_city')
]
