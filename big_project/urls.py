"""big_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from basic_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index ,name='index'),
    path('main/',views.main,name='main'),
    path('login/',views.user_login,name='login'),
    path('register/',views.register,name='register'),
    path('patient_reg/',views.patient_reg.as_view(),name='patient_reg'),
    path('doctor_reg/',views.doctor_reg.as_view(),name='doctor_reg'),
    path('doctor_dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('diet/',views.diet,name='diet'),
    path('health-insurance/',views.insurance,name='insurance'),
    path('delapp/<int:pk>/',views.deleteApp,name='deleteApp'),
    path('editapp/<int:pk>/',views.editApp,name='editApp'),
    path('deldocapp/<int:pk>/',views.delDocApp,name='delDocApp'),
    path('prescription/<int:pk>/',views.prescription,name='prescription'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download'),
    path('download-patient/<int:pk>', views.download_patient,name='download_patient'),
    path('download-doctor/<int:pk>', views.download_doctor,name='download_doctor'),
    path('logout/',views.user_logout,name='logout'),
]
