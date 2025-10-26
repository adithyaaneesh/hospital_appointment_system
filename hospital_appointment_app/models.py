from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Credentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=20,default='DefaultName')
    email = models.EmailField(max_length=50, blank=True, null=True)
    phonenumber = models.CharField(max_length=20,  blank=True, null=True)

    ROLE_CHOICES = [
        ("user", 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.firstname} - {self.role}"


class Doctor(models.Model):
    name =  models.CharField(max_length=25)
    specialty = models.CharField(max_length=30)
    available_time = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.specialty}"

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
]

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    patient_name = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name} - {self.date} - {self.time_slot}"
