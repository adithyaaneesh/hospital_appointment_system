from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('book_appointment', views.book_appointment, name='book_appointment'),
    path('appointment-history', views.appointment_history, name='appointment_history'),
    path('manage_appointment/', views.manage_appointment, name='manage_appointment'),
    path('approve/<int:appointment_id>/', views.approve_request, name='approve_request'),
    path('reject/<int:appointment_id>/', views.reject_request, name='reject_request'),    
    path('doctors', views.doctor, name='doctors'),
]

