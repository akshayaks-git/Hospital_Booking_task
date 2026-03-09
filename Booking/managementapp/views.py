from django.shortcuts import *
# from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import authenticate, login,logout
from django.utils import timezone

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# Create your views here.
from .models import Doctor,Appointment,Patient,User, Doctor, DoctorLeave

from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from datetime import date, timedelta, datetime
from datetime import datetime as dt_datetime

from datetime import date as dt_date
from django.utils.timezone import now
from django.urls import reverse


def Base(request):
    return render(request, "base.html")
def index(request):
    return render(request,'index.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')


        try:
            # First check if user exists and is active
            user = User.objects.get(username=username)
            
           
                
            # Then authenticate the user
            authenticated_user = authenticate(request, username=username, password=password)
            
            if authenticated_user is None:
                return JsonResponse({
                    'status': 'error',
                    'message': 'You are not registered as a patient.'
                }, status=401)

            # User is authenticated and active - proceed with login
            login(request, authenticated_user)
            
            # Check user type and redirect accordingly
            if authenticated_user.is_superuser:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Welcome, Admin!',
                    'redirect_url': '/admin_home'
                }, status=200)
            elif authenticated_user.is_staff:
                try:
                    Doctor.objects.get(user=authenticated_user)
                    request.session['doctor_id'] = authenticated_user.id
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Welcome, Doctor!',
                        'redirect_url': '/doctor_home'
                    }, status=200)
                except Doctor.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Doctor profile not found'
                    }, status=400)
            else:
                try:
                    Patient.objects.get(user=authenticated_user)
                    request.session['patient_id'] = authenticated_user.id
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Login successful!',
                        'redirect_url': '/patient_home'
                    }, status=200)
                except Patient.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Patient profile not found'
                    }, status=400)

        except User.DoesNotExist:
            # Generic error message for security (don't reveal if user exists)
            return JsonResponse({
                'status': 'error',
                'message': 'You are not registered as a patient.'
            }, status=401)

    return render(request, 'login.html')

def doctor_home(request):
    return render(request,'doctor_home.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def admin_home(request):
    patient_count=Patient.objects.count()
    return render(request, 'admin_home.html', {'patient_count':patient_count})


def appointments_list(request):
    today = timezone.localdate()

    # Appointments for today
    todays_appointments = Appointment.objects.select_related('patient', 'doctor').filter(booking_date=today).order_by('time_slot')

    # All appointments
    all_appointments = Appointment.objects.select_related('patient', 'doctor').all().order_by('-booking_date', 'time_slot')

    # Counts
    total_todays = todays_appointments.count()
    total_all = all_appointments.count()

    return render(request, 'admin_appointments_today.html', {
        'todays_appointments': todays_appointments,
        'all_appointments': all_appointments,
        'total_todays': total_todays,
        'total_all': total_all,
        'today': today,
    })


def patient_list(request):
    # Fetch all patients
    patients = Patient.objects.all()
    
    # Count total patients
    total_patients = patients.count()
    
    # Render the template
    return render(request, 'patient_list.html', {
        'patients': patients,
        'total_patients': total_patients
    })





def delete_patient(request, patient_id):
    if request.method == "POST":
        patient = get_object_or_404(Patient, id=patient_id)
        user = patient.user
        patient.delete()
        user.delete()
        messages.success(request, "Patient deleted successfully.")
    return redirect('patient_list')


    



def patient_home(request):
    return render(request, "patient_home.html")
def patient_register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')

        if not username or not password or not name or not address or not email or not phone_number or not date_of_birth:
            messages.error(request, "All fields are required")
            return redirect('patient_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('patient_register')

        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=True,
            usertype='Patient'
        )

        Patient.objects.create(
            user=user,
            name=name,
            address=address,
            email=email,
            phone_number=phone_number,
            date_of_birth=date_of_birth
        )

        messages.success(request, "🎉 Patient Registered Successfully!")
        return redirect('patient_register')

    return render(request, 'patient_register.html')
# view patient profile


@login_required
def patient_profile(request):
    # Fetch the patient object linked to the currently logged-in user
    patient = get_object_or_404(Patient, user=request.user)

    return render(request, 'patient_profileview.html', {
        'view': patient,
        'data': request.user
    })



def register_doctor(request):
    success = False

    if request.method == 'POST':
        name = request.POST.get('name')
        doc_spec = request.POST.get('doc_spec')
        email=request.POST.get('email')
        medical_department = request.POST.get('medical_department')
        qualification = request.POST.get('qualification')
        phone_number=request.POST.get('phone_number')
        photo = request.FILES.get('photo')
        username = request.POST.get('username')  
        password = request.POST.get('password')

        # Validation
        if not username or not password or not name:
            messages.error(request, "Please fill all required fields!")
            return render(request, 'register_doctor.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'register_doctor.html')

        user = User.objects.create_user(
            username=username,
            password=password,
            usertype='Doctor',
            is_staff=True,
            is_active=True
        )

        Doctor.objects.create(
            user=user,
            name=name,
            doc_spec=doc_spec,
            email=email,
            phone_number=phone_number,
            medical_department=medical_department,
            qualification=qualification,
            photo=photo
        )

        success = True

    return render(request, 'register_doctor.html', {'success': success})



def appointment_list(request):
    appointments = Appointment.objects.all()
    print("Appointments:", appointments)  # check console output
    return render(request, 'appointment_list.html', {'appointments': appointments})

def appointment_list(request):
    appointments = Appointment.objects.filter(p_email=request.user.email)
    return render(request, 'appointment_list.html', {'appointments': appointments})



def departments(request):
    return render(request, "department_list.html")



def contact(request):
      return render(request,"contact.html")
def about(request):
    return render(request,"about.html")
def about_view(request):
    print("Current URL:", request.path)
    return render(request, 'about.html')
def admin_home(request):
    return render(request,"admin_home.html")


# Doctor profile view

def Doctor_profile(request):
    doc_id = request.session.get('doctor_id')
    doctor = Doctor.objects.get(user_id=doc_id)
    user = User.objects.get(id=doc_id)
    return render(request, 'doctor_profile_view.html', {
        'view': doctor,
        'data': user
    })

def view_profile(request):
    return render(request,"doctor_profile_view.html")

def edit_profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    user = doctor.user

    if request.method == 'POST':
        # Update User
        username = request.POST.get('username', '').strip()
        if username:
            user.username = username

        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.save()

        # Update Doctor safely
        doctor.name = request.POST.get('name', '').strip()
        doctor.doc_spec = request.POST.get('doc_spec', '').strip()
        doctor.qualification = request.POST.get('qualification', '').strip()
        doctor.medical_department = request.POST.get('medical_department', '').strip()

        # Safe numeric conversion
        consultation_fee = request.POST.get('consultation_fee')
        doctor.consultation_fee = float(consultation_fee) if consultation_fee else 0.0

        # Optional photo
        if request.FILES.get('photo'):
            doctor.photo = request.FILES.get('photo')

        # Optional fields if you added email and phone
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone_number', '').strip()
        if hasattr(doctor, 'email'):
            doctor.email = email
        if hasattr(doctor, 'phone_number'):
            doctor.phone_number = phone

        # Validate required fields
        if not doctor.qualification:
            messages.error(request, "Qualification is required!")
            return redirect('update_doctor', doctor_id=doctor.id)

        doctor.save()
        messages.success(request, "Doctor updated successfully!")
        return redirect('admin_home')

    return render(request, 'doctor_profile_edit.html', {'doctor': doctor, 'user': user})



def booking(request):
    doctors = Doctor.objects.all()  
    return render(request, 'booking.html', {
        'doctors': doctors
    })

def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    user = doctor.user
    doctor.delete()
    user.delete()
    messages.success(request, "Doctor deleted successfully!")
    return redirect('admin_home')





def confirm_appointment(request, doctor_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "⚠️ Please log in to book an appointment."})

    if request.method == "POST":
        booking_date_str = request.POST.get("booking_date")
        time_slot = request.POST.get("time_slot")

        from datetime import datetime
        booking_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()

        doctor = get_object_or_404(Doctor, id=doctor_id)
        patient = get_object_or_404(Patient, user=request.user)

        # ❌ If patient already booked any slot with this doctor on this date
        if Appointment.objects.filter(doctor=doctor, patient=patient, booking_date=booking_date).exists():
            return JsonResponse({
                "status": "error",
                "message": f"⚠️ You already have an appointment with Dr. {doctor.name} on {booking_date}."
            })

        # ❌ If the selected slot is already taken by someone else
        if Appointment.objects.filter(doctor=doctor, booking_date=booking_date, time_slot=time_slot).exists():
            return JsonResponse({
                "status": "error",
                "message": f"❌ {time_slot} on {booking_date} is already booked."
            })

        # ✅ Create appointment
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            booking_date=booking_date,
            time_slot=time_slot,
            is_confirmed=True,
            contact_number=getattr(patient, "phone_number", None),
        )

        return JsonResponse({
            "status": "success",
            "message": f"✅ Appointment booked with Dr. {doctor.name} at {time_slot} on {booking_date}."
        })

    return JsonResponse({"status": "error", "message": "Invalid request"})
@login_required
def my_appointments(request):
    patient = Patient.objects.get(user=request.user)  # get the Patient object
    appointments = Appointment.objects.filter(patient=patient).select_related('doctor').order_by('booking_date')
    return render(request, 'my_appointments.html', {'appointments': appointments})



@login_required
def cancel_appointment(request,id):
    appointment = get_object_or_404(Appointment, id=id, patient__user=request.user)
    appointment.is_confirmed = False
    appointment.save()
    messages.success(request, "Appointment cancelled successfully.")
    return redirect('my_appointments')

# doctor appoinment
@login_required
def doctor_appointments(request):
    doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('booking_date', 'time_slot')
    return render(request, 'doctor_appointments.html', {'appointments': appointments})





def doctors(request):
    return render(request,"doctor_list.html")


def mark_leave(request, doctor_id=None):
    # get doctor (from URL or session)
    if not doctor_id:
        user_id = request.session.get('doctor_id')
        doctor = get_object_or_404(Doctor, user_id=user_id)
    else:
        doctor = get_object_or_404(Doctor, id=doctor_id)

    leave = None
    booking_date_str = request.GET.get('date')  # allows ?date=YYYY-MM-DD to load existing leave

    if request.method == "POST":
        leave_date = request.POST.get("date")
        morning = request.POST.get("morning") == "on"
        afternoon = request.POST.get("afternoon") == "on"
        full_day = request.POST.get("full_day") == "on"

        # if full_day checked, store both sessions as True
        if full_day:
            morning = True
            afternoon = True

        DoctorLeave.objects.update_or_create(
            doctor=doctor,
            date=leave_date,
            defaults={"morning": morning, "afternoon": afternoon}
        )

        messages.success(request, "✅ Leave submitted successfully!")
        # redirect back to the same page with the date param so the saved leave is loaded and shown
        return redirect(reverse('mark_leave', kwargs={'doctor_id': doctor.id}) + f'?date={leave_date}')

    # GET: if date param provided, try to load existing leave for that date
    booking_date = None
    if booking_date_str:
        try:
            booking_date = dt_date.fromisoformat(booking_date_str)
        except Exception:
            booking_date = None

    if booking_date:
        leave = DoctorLeave.objects.filter(doctor=doctor, date=booking_date).first()

    return render(request, "mark_leave.html", {
        "doctor": doctor,
        "leave": leave,
        "booking_date": booking_date_str
    })


@login_required
def admin_home(request):
    doctors = Doctor.objects.all()
    today = now().date()

    doctor_status = []
    for doc in doctors:
        leave = DoctorLeave.objects.filter(doctor=doc, date=today).first()
        if leave:
            status = leave.status()   # using DoctorLeave.status() method
        else:
            status = "✅ Available"

        doctor_status.append({
            "doctor": doc,
            "status": status
        })

    return render(request, "admin_home.html", {"doctor_status": doctor_status})





# Mark appointment as completed (AJAX for doctor)
@login_required
@require_POST
def mark_completed(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor__user=request.user)
    if not appointment.remarks:
        appointment.remarks = "Visit completed"
        appointment.save()
    return JsonResponse({"success": True, "appointment_id": appointment.id, "status": "Completed"})

# Patient API to return minimal appointment statuses
@login_required
def patient_appointments_api(request):
    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient=patient)
    data = []
    for a in appointments:
        if not a.is_confirmed:
            status = "Cancelled"
        elif a.remarks:
            status = "Completed"
        else:
            status = "Waiting"
        data.append({"id": a.id, "status": status})
    return JsonResponse({"appointments": data})


@login_required
def doctor_appointments_api(request):
    doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('booking_date', 'time_slot')

    data = []
    for appt in appointments:
        if not appt.is_confirmed:
            status = "Cancelled"
        elif appt.remarks:
            status = "Completed"
        else:
            status = "Waiting"

        data.append({
            "id": appt.id,
            "patient": appt.patient.name,
            "date": appt.booking_date.strftime("%Y-%m-%d") if appt.booking_date else "",
            "time_slot": appt.time_slot,
            "status": status,
        })

    return JsonResponse({"appointments": data})



def booking_view(request, doctor_id=None):
    doctors = Doctor.objects.all()
    doctor = None
    booking_date = None
    availability = []
    available_slots = []
    disabled_slots = []

    # If doctor is selected
    if doctor_id:
        doctor = get_object_or_404(Doctor, id=doctor_id)
    else:
        doctor_id = request.GET.get("doctor_id")
        if doctor_id:
            doctor = get_object_or_404(Doctor, id=doctor_id)

    # Generate next 7 days availability
    if doctor:
        today = date.today()
        days = [today + timedelta(days=i) for i in range(7)]

        leave_records = DoctorLeave.objects.filter(doctor=doctor, date__in=days)
        leave_map = {leave.date: leave for leave in leave_records}

        for d in days:
            leave = leave_map.get(d)
            if leave:
                morning_status = "❌ Leave" if leave.morning else "✅ Available"
                afternoon_status = "❌ Leave" if leave.afternoon else "✅ Available"
            else:
                if doctor.available:
                    morning_status = afternoon_status = "✅ Available"
                else:
                    morning_status = afternoon_status = "❌ Leave"

            availability.append({
                "date": d,
                "morning_status": morning_status,
                "afternoon_status": afternoon_status
            })

    # If date selected → show available time slots
    date_str = request.GET.get("date")
    if doctor and date_str:
        booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()


        all_slots = [
            ("10:00 AM", "morning"),
            ("10:30 AM", "morning"),
            ("11:00 AM", "morning"),
            ("11:30 AM", "morning"),
            ("12:00 PM", "morning"),
            ("02:00 PM", "afternoon"),
            ("02:30 PM", "afternoon"),
            ("03:00 PM", "afternoon"),
            ("03:30 PM", "afternoon"),
            ("04:00 PM", "afternoon"),
            ("04:30 PM", "afternoon"),
            ("05:00 PM", "afternoon"),
        ]

        leave = DoctorLeave.objects.filter(doctor=doctor, date=booking_date).first()
        if leave:
            if leave.morning:
                disabled_slots += [s for s, session in all_slots if session == "morning"]
            if leave.afternoon:
                disabled_slots += [s for s, session in all_slots if session == "afternoon"]

        booked_slots = Appointment.objects.filter(
            doctor=doctor, booking_date=booking_date
        ).values_list("time_slot", flat=True)

        disabled_slots = set(disabled_slots) | set(booked_slots)
        available_slots = [s for s, _ in all_slots if s not in disabled_slots]

    return render(request, "booking.html", {
        "doctors": doctors,
        "doctor": doctor,
        "availability": availability,
        "booking_date": booking_date,
        "available_slots": available_slots,
        "disabled_slots": disabled_slots
    })
