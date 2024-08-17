"""
URL configuration for regulatory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from regulator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.regulation_list, name='regulation_list'),
    path('<int:pk>/', views.regulation_detail, name='regulation_detail'),
    path('regulation/<int:pk>/pdf/', views.regulation_detail_pdf, name='regulation_detail_pdf'),
    path('regulators/', views.regulator_list, name='regulator_list'),
    path('regulators/<int:pk>/', views.regulator_detail, name='regulator_detail'),
]
