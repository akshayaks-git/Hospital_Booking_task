# Hospital Booking System

## Overview
The Hospital Booking System is a web application that allows patients to book appointments with doctors and enables administrators and doctors to manage doctors, patients, and appointments. The system provides a simple interface to handle hospital scheduling and basic data management.

The purpose of this project is to demonstrate the implementation of a functional booking system with proper data handling, validation, and user interface.

---

## Objective
The objective of this system is to:

- Allow patients to register and store their information.
- Enable administrators to manage doctor details.
- Allow patients to book appointments with doctors.
- Allow doctors to view their patient appointments.
- Allow doctors to update their availability or take leave.
- Prevent booking when the doctor is unavailable or on leave.
- Prevent double booking of the same time slot.
- Provide an interface to view and manage appointments.

---

## Technology Stack

**Backend**
- Python  
- Django  

**Frontend**
- HTML  
- CSS  
- Bootstrap  

**Database**
- SQLite  

---

## Features

### Patient Registration
Patients can register in the system with the following details:

**Required Fields**
- Patient Name  
- Email  
- Phone Number  

**Optional Fields**
- Date of Birth  
- Address  

**Functions**
- Register new patient  
- View patient details  
- Email and phone number validation  

---

### Doctor Management

Administrators can manage doctors in the system.

**Add Doctor**
- Doctor Name  
- Specialization  
- Email  
- Phone Number  
- Consultation Fee  
- Available Days  

**Update Doctor**
- Modify doctor details  

**Delete Doctor**
- Remove doctor from the system  

**View Doctors**
- Display all doctors with specialization and availability  

---

### Doctor Availability Management

Doctors can manage their availability.

**Features**
- Doctors can view their patient appointments
- Doctors can update available days and time slots
- Doctors can mark leave days
- Patients cannot book appointments during doctor leave or unavailable time slots

---

### Appointment Booking

Patients can book appointments with doctors.

**Booking Steps**
1. Select doctor  
2. Choose available date  
3. Select time slot  
4. Confirm appointment  

**Constraints**
- Prevent double booking for the same doctor and time slot.
- Prevent booking if the doctor is on leave or unavailable.

**Appointment Details**
- Patient  
- Doctor  
- Appointment Date  
- Time Slot  
- Booking Status (Booked / Cancelled)  

---

### Appointment Management

The system allows management of all appointments.

**Features**
- View all appointments  
- Filter appointments by doctor, date, or patient  
- Cancel appointment  
- View upcoming appointments  

---

### Admin Dashboard (Optional)

The dashboard provides a summary of system activity:

- Total number of doctors  
- Total number of patients  
- Total number of appointments  
- Appointments scheduled for today  

---

## Database Models

### Patient
Stores patient information.

### Doctor
Stores doctor details including specialization and availability.

### Appointment
Stores appointment booking details between patients and doctors.
