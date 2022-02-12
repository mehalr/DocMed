from django.shortcuts import render

import basic_app
from django.http import request
from django.urls import reverse
from basic_app.form import *
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context

from basic_app.whatsapp import send_message
from basic_app import models
from basic_app.models import * 
import pickle 
import joblib
import csv

# Create your views here.

def index(request):
	return render(request,'basic_app/index.html')



def register(request):

	return render(request,'basic_app/register.html')

class patient_reg(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'basic_app/patient_reg.html'

    def form_valid(self, form):
        user = form.save()
        return HttpResponseRedirect(reverse('login'))

class doctor_reg(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'basic_app/doctor_reg.html'

    def form_valid(self, form):
        user = form.save()
        return HttpResponseRedirect(reverse('login'))


def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request,username=username,password=password)

		if user is not None:
			if user.is_active and user.is_doctor:
				print(user.username)
				login(request,user)
				return HttpResponseRedirect(reverse('doctor_dashboard')) 
			elif user.is_active and user.is_patient:
				print(user.username)
				login(request,user)
				return HttpResponseRedirect(reverse('patient_dashboard'))      

			else:
				HttpResponse("ACCOUNT NOT ACTIVE")

		else:
			print("Someone tried to login but failed")
			print("Username: {} \nPassword: {}".format(username,password))
			messages.error(request,"Username or Password incorrect!")
			return HttpResponseRedirect(reverse('login')) 

	else:
		return render(request,'basic_app/login.html')




@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



    
        
         

	


