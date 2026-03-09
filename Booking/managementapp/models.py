from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Custom User Model
class User(AbstractUser):
    usertype = models.CharField(max_length=100)

# Patient Model
class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField()
    # age = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='patients'
    )



    



class Doctor(models.Model):
    name = models.CharField(max_length=100)
    doc_spec = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    qualification = models.CharField(max_length=200, help_text="E.g., MBBS, MD, PhD")
    photo = models.ImageField(upload_to='doctor_photos/', blank=True, null=True)
    medical_department = models.CharField(max_length=100)
    consultation_fee = models.DecimalField(
    max_digits=8, decimal_places=2, default=500.00,
    help_text="Fee in your currency"
)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.name} - ({self.doc_spec})"

# Appointment Model



class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name='appointments')
    
    booking_date = models.DateField(null=True, blank=True)
    booked_on = models.DateField(auto_now_add=True)
    time_slot = models.CharField(max_length=20, null=True, blank=True)
    
    is_confirmed = models.BooleanField(default=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.name} with {self.doctor} on {self.booking_date}"
    

class DoctorLeave(models.Model):
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE)
    date = models.DateField()
    morning = models.BooleanField(default=True)   # True = available
    afternoon = models.BooleanField(default=True) # True = available

    class Meta:
        unique_together = ("doctor", "date")  # avoid duplicate leave for same date

    def __str__(self):
        return f"{self.doctor.name} - {self.date} (M:{self.morning}, A:{self.afternoon})"

    def status(self):
        if not self.morning and not self.afternoon:
            return "❌ Full Day Leave"
        elif not self.morning:
            return "☀️ Morning Leave"
        elif not self.afternoon:
            return "🌙 Afternoon Leave"
        return "✅ Available"