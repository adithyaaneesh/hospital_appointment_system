from django.db import models

# Create your models here.

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
    patient_name = models.CharField(max_length=25)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time_slot = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name} - {self.date} - {self.time_slot}"
