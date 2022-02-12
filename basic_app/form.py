from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from basic_app.models import *
from basic_app import models
# from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

number = RegexValidator(r'^[0-9]*$',"Only Numbers Allowed")




class DoctorSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True,validators=[number],max_length=10,min_length=10)
    speciality = forms.CharField(required=True)
    

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.phone_number=self.cleaned_data.get('phone_number')
        doctor.speciality=self.cleaned_data.get('speciality')
        doctor.save()
        return user

class PatientSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True,validators=[number],max_length=10,min_length=10)
    location = forms.CharField(required=True)


    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        patient = Patient.objects.create(user=user)
        patient.phone_number=self.cleaned_data.get('phone_number')
        patient.location=self.cleaned_data.get('location')
        patient.save()
        return user

