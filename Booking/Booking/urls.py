"""
URL configuration for Booking project.

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
from django.contrib import admin
from django.urls import path
# from .import views
from managementapp import views
from django.contrib.auth import views as auth_views
# from .views import add_department, department_list
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    path('base/', views.Base,name='base'),
    path('base/login',views.login_view,name='login'),
    path('login/admin_home',views.admin_home,name='admin_home'),
    path('admin_home/', views.admin_home, name='admin_home'),

    # all logouts
      path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
  
    path('login/',views.login_view,name='login'),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('login/patient_home', views.patient_home, name='patient_home'),
    path('patient_home/', views.patient_home, name='patient_home'),
# view patient profile
    path('patient_profile/', views.patient_profile, name='patient_profile'),
    path('view_patient/patient_list', views.patient_list, name='patient_list'),
# booking
    path('booking/', views.booking, name='booking'),
#appoinment
    path('appoints/', views.appointment_list, name='appointment_list'),
    path('patient_home/appoints',views.appointment_list,name='appointment_list'),
       
    path('base/departments/', views.departments, name='departments'),
    path('departments/', views.departments, name='department_list'),
    path('about/', views.about,name='about'),
    path('base/register_doctor', views.register_doctor, name='register_doctor'),
    path('register_doctor/', views.register_doctor, name='register_doctor'),
    path('login/doctor_home', views.doctor_home, name='doctor_home'),
    path('doctor_home/', views.doctor_home, name='doctor_home'),

    path("logout/", LogoutView.as_view(), name="logout"),


    path('patient/',views.patient_list,name='patients_list'),
    path('delete-patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
# doctor profile view
    path('doctor_profile/', views.Doctor_profile, name='doctor_profile'),
    path('doctor/profile/', views.Doctor_profile, name='doctor_profile'),
# doctor edit profile
    path('edit_profile/', views.edit_profile, name='edit_profile'),

#view doctors
    path('doctors/', views.doctors, name='doctors'),
    path('patient_home/doctor', views.doctors, name='doctors'),

# my appointment
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('doctor/profile/edit/<int:doctor_id>/', views.edit_profile, name='update_doctor'),
    path('doctor/delete/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),


# doctor appointment
   path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
   path('doctor_appointments/', views.doctor_appointments, name='doctor_appointments'),
# doctor avalability
   
   path("doctors/", views.doctors, name="doctors"),
   
    # Doctor leave page
    path("doctor/<int:doctor_id>/mark-leave/", views.mark_leave, name="mark_leave"),
    path("doctor/mark-leave/", views.mark_leave, name="mark_leave"),
    path('book_appointment/', views.booking_view, name='book_appointment'),

    path("confirm_appointment/<int:doctor_id>/", views.confirm_appointment, name="confirm_appointment"),
    path("my_appointments/", views.my_appointments, name="my_appointments"),
    # Doctor AJAX endpoint
    path('doctor/appointment/<int:appointment_id>/completed/', views.mark_completed, name='mark_completed'),
    path('doctor/appointments/api/', views.doctor_appointments_api, name='doctor_appointments_api'),
    # API for patient polling
    path('patient/appointments/api/', views.patient_appointments_api, name='patient_appointments_api'),

    # Cancel appointment (POST)
    # urls.py
    path('appointment/<int:id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    
    path('admin_home/appointments_list/', views.appointments_list, name='appointments_list'),



    path('booking/', views.booking_view, name='booking'),
    path('booking/<int:doctor_id>/', views.booking_view, name='booking_with_doctor'),

    # Mark leave page
    path('mark-leave/', views.mark_leave, name='mark_leave'),
    path('mark-leave/<int:doctor_id>/', views.mark_leave, name='mark_leave_with_doctor'),

    ]







urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
