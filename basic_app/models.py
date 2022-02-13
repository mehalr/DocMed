from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from django.core.validators import RegexValidator

numeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')


class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50,blank=True)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    phone_number = models.CharField(max_length=20,validators=[numeric])
    speciality = models.CharField(max_length=20)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    phone_number = models.CharField(max_length=20,validators=[numeric])
    location = models.CharField(max_length=20)

class Appointments(models.Model):

    First_name = models.CharField(max_length=20)
    Last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20,validators=[numeric])
    doctor = models.CharField(max_length=20)
    message = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    date = models.CharField(max_length=20)
    patient_username = models.CharField(max_length=20,default="")
    doctor_username= models.CharField(max_length=20,default="")
    # prescription_status = models.CharField(max_length=20,blank=True)
    objects=models.Manager()

    def __str__(self):
        return self.First_name

class DoctorProfile(models.Model):

    full_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    speciality = models.CharField(max_length=20)
    qualification = models.CharField(max_length=20)
    location =models.CharField(max_length=20)
    hospital_name = models.CharField(max_length=20)
    doctor_username =models.CharField(max_length=20,default="")

    objects=models.Manager()

    def __str__(self):
        return self.full_name

class Prescription(models.Model):

    patientid = models.PositiveIntegerField(null=True)

    patient_username = models.CharField(max_length=20,default="")


    patientName= models.CharField(max_length=20)
    patientPhone = models.CharField(max_length=20)
    appointmentDate = models.CharField(max_length=20)

    doctorName = models.CharField(max_length=20)

    symptom= models.CharField(max_length=40)
    medicine= models.CharField(max_length=50)

    doctorFee= models.PositiveIntegerField(null=False)
    medicineFee= models.PositiveIntegerField(null=False)
    otherCharges = models.PositiveIntegerField(null=False)
    total= models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.patientName






       
