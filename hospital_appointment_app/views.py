from django.shortcuts import get_object_or_404, redirect, render
from .models import Appointment, Doctor
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm



def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  

            if user.is_superuser:
                return redirect('dashboard')  
            return redirect('index')

        return render(request, "login.html", {'error': 'Invalid username or password'})

    return render(request, "login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def index(request):
    return render(request, 'index.html')

@login_required
def doctor(request):
    if request.method == 'POST':
        Doctor.objects.create(
            name=request.POST.get('name'),
            specialty=request.POST.get('specialty'),
            available_time=request.POST.get('available_time')
        )
        return redirect('index')
    return render(request, 'doctors.html')

@login_required
def book_appointment(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        doctor_name = request.POST.get('doctor') 
        try:
            doctor = Doctor.objects.get(name=doctor_name)
        except Doctor.DoesNotExist:
            messages.error(request, f'Doctor "{doctor_name}" not found.') 
            return render(request, 'book_appointment.html', {'doctors': doctors})

        Appointment.objects.create(
            user=request.user,
            patient_name=request.POST.get('patient_name'),
            doctor=doctor,
            date=request.POST.get('date'),
            time_slot=request.POST.get('time_slot'),
            status='Pending',
        )

        messages.success(request, f'Appointment booked successfully with Dr. {doctor.name}!')
        return redirect('book_appointment')

    return render(request, 'book_appointment.html', {'doctors': doctors})

@login_required
def appointment_history(request):
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'appointment_history.html', {
        'doctors': doctors,
        'appointments': appointments,
    })


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def manage_appointment(request):
    requests_list = Appointment.objects.all().order_by('-created_at')
    return render(request, 'manage_appointment.html', {'requests': requests_list})

@login_required
def approve_request(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Confirmed'
    appointment.save()
    messages.success(request, f'Appointment for {appointment.patient_name} confirmed.')
    return redirect('manage_appointment')

@login_required
def reject_request(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Cancelled'
    appointment.save()
    messages.error(request, f'Appointment for {appointment.patient_name} cancelled.')
    return redirect('manage_appointment')