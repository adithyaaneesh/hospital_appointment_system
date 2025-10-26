from django.shortcuts import redirect, render
from .models import Appointment, Doctor

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
        doctor_id = request.POST.get('doctor')
        doctor = Doctor.objects.get(id=doctor_id)

        Appointment.objects.create(
            patient_name=request.POST.get('patient_name'),
            doctor=doctor,
            date=request.POST.get('date'),
            time_slot=request.POST.get('time_slot'),
            status='pending',
        )
        return redirect('index')
    return render(request, 'book_appointment.html', {'doctors': doctors})