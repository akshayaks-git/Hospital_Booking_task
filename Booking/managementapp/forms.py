from django import forms
from django.contrib.auth.models import User

from .models import Appointment,Doctor,Patient



# class DoctorRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Doctor
#         fields = ['name', 'doc_spec', 'qualification', 'photo', 'medical_department', 'user', 'available']
 





#     def save(self, commit=True):
#         user = User.objects.create_user(
#             username=self.cleaned_data['username'],
#             email=self.cleaned_data['email'],
#             password=self.cleaned_data['password']
#         )
#         doctor = super().save(commit=False)
#         doctor.user = user
#         if commit:
#             doctor.save()
#         return doctor
    
# class PatientForm(forms.ModelForm):
#     class Meta:
#         model=Patient
#         fields=['name','address','phone_number','date_of_birth','age','user']