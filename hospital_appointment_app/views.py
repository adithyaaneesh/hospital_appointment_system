from django.shortcuts import get_object_or_404, redirect, render
from .models import Appointment, Doctor
from django.contrib import messages


# Create your views here.

def index(request):
    return render(request, 'index.html')

def doctor(request):
    if request.method == 'POST':
        Doctor.objects.create(
            name=request.POST.get('name'),
            specialty=request.POST.get('specialty'),
            available_time=request.POST.get('available_time')
        )
        return redirect('index')
    return render(request, 'doctors.html')


def book_appointment(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        doctor_name = request.POST.get('doctor') 
        try:
            doctor = Doctor.objects.get(name=doctor_name)
        except Doctor.DoesNotExist:
            messages.error(request, f'Doctor "{doctor_name}" not found.')  # ❌ Error
            return render(request, 'book_appointment.html', {'doctors': doctors})

        Appointment.objects.create(
            patient_name=request.POST.get('patient_name'),
            doctor=doctor,
            date=request.POST.get('date'),
            time_slot=request.POST.get('time_slot'),
            status='Pending',
        )
        messages.success(request, f'Appointment booked successfully with Dr. {doctor.name}!')  # ✅ Success
        return redirect('index')

    return render(request, 'book_appointment.html', {'doctors': doctors})

def appointment_history(request):
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all().order_by('-created_at')

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        doctor = Doctor.objects.get(id=doctor_id)

        Appointment.objects.create(
            patient_name=request.POST.get('patient_name'),
            doctor=doctor,
            date=request.POST.get('date'),
            time_slot=request.POST.get('time_slot'),
            status='Pending',
        )
        return redirect('appointment_history')

    return render(request, 'appointment_history.html', {
        'doctors': doctors,
        'appointments': appointments,
    })

def dashboard(request):
    return render(request, 'dashboard.html')

def manage_appointment(request):
    requests_list = Appointment.objects.all().order_by('-created_at')
    return render(request, 'manage_appointment.html', {'requests': requests_list})

def approve_request(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Confirmed'
    appointment.save()
    messages.success(request, f'Appointment for {appointment.patient_name} confirmed.')
    return redirect('manage_appointment')

def reject_request(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Cancelled'
    appointment.save()
    messages.error(request, f'Appointment for {appointment.patient_name} cancelled.')
    return redirect('manage_appointment')