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
def patient_dashboard(request):

	docname = DoctorProfile.objects.all()

	delapp = Appointments.objects.all()

	app= Appointments.objects.filter(patient_username=request.user.username)
	
	finddoctor=''

	pres = Prescription.objects.filter(patient_username=request.user.username)
	print(app)
   
	if request.method == 'POST':

		if 'appointment' in request.POST:
			First_name=request.POST.get('First_name')
			Last_name=request.POST.get('Last_name')
			phone_number=request.POST.get('phone_number')
			doctor=request.POST.get('doctor')
			message=request.POST.get('message')
			time=request.POST.get('time')
			date=request.POST.get('date')
			patient_username= request.user.username
			doc = DoctorProfile.objects.filter(full_name=doctor)
			print(doc)
			doctor_username = doc[0].doctor_username


			try:
				booking_form=Appointments(First_name=First_name,Last_name=Last_name,phone_number=phone_number,
					doctor=doctor,message=message,time=time,date=date,patient_username=patient_username,
					doctor_username=doctor_username)
				booking_form.save()
				send_message(f'Your appointment has been scheduled with {doctor} on {date} at {time}')
				print('success')
				return HttpResponseRedirect(reverse('patient_dashboard'))
			except:
				print('not successful :( ')

		elif 'finddoc' in request.POST:

			location = request.POST.get('location')
			speciality = request.POST.get('speciality')

			finddoctor = DoctorProfile.objects.filter(location=location,speciality=speciality)

			if (finddoctor.count()==0):
				finddoctor=None




	context = {'app':app,'docname':docname,'finddoctor':finddoctor,'delapp':delapp,'pres':pres}


	return render(request,'basic_app/patient_dashboard.html',context)

@login_required
def editApp(request,pk):

	docname = DoctorProfile.objects.all()

	editapp = Appointments.objects.get(id=pk)


	if 'appointment' in request.POST:
			First_name=request.POST.get('First_name')
			Last_name=request.POST.get('Last_name')
			phone_number=request.POST.get('phone_number')
			doctor=request.POST.get('doctor')
			message=request.POST.get('message')
			time=request.POST.get('time')
			date=request.POST.get('date')


			Appointments.objects.filter(id=pk).update(First_name=First_name,Last_name=Last_name,
				phone_number=phone_number,doctor=doctor,message=message,time=time,date=date)

			return HttpResponseRedirect(reverse('patient_dashboard'))

	context={'editapp':editapp,'docname':docname}

	return render(request,'basic_app/editapp.html',context) 

@login_required
def deleteApp(request,pk):

	delapp = Appointments.objects.get(id=pk)
	print(delapp)
	
	delapp.delete()
	return HttpResponseRedirect(reverse('patient_dashboard'))

@login_required
def doctor_dashboard(request):


	docapp = Appointments.objects.filter(doctor_username=request.user.username)
	cnt = docapp.count()

	pres=[]

	if docapp:
		pres = Prescription.objects.filter(doctorName=docapp[0].doctor)

	app = []
	pre = []


	for a in docapp:
		v = 0
		for p in pres:
			if a.id==p.patientid:
				print('patid',p.patientid)
				v=1
				pre.append(a.id)

		if v==0:
			print('aid',a.id)
			app.append(a.id)



	if DoctorProfile.objects.filter(doctor_username=request.user.username):
		profile = DoctorProfile.objects.get(doctor_username=request.user.username)
	else:
		profile=None



	context={'docapp':docapp,'cnt':cnt,'pres':pres,'profile':profile,'app':app,'pre':pre}

	if request.method=="POST":

		if not profile:

			full_name=request.POST.get('full_name')
			phone_number=request.POST.get('phone_number')
			speciality=request.POST.get('speciality')
			qualification=request.POST.get('qualification')
			location=request.POST.get('location')
			hospital_name=request.POST.get('hospital_name')
			doctor_username= request.user.username

			try:
				profile_form=DoctorProfile(full_name=full_name,phone_number=phone_number,
					speciality=speciality,qualification=qualification,location=location,hospital_name=hospital_name,
					doctor_username=doctor_username)
				profile_form.save()
				print('success')
				return HttpResponseRedirect(reverse('doctor_dashboard'))
			except:
				print('not successful :( ')
		else:
			full_name=request.POST.get('full_name')
			phone_number=request.POST.get('phone_number')
			speciality=request.POST.get('speciality')
			qualification=request.POST.get('qualification')
			location=request.POST.get('location')
			hospital_name=request.POST.get('hospital_name')
			doctor_username= request.user.username

			try:
				DoctorProfile.objects.filter(id=profile.id).update(full_name=full_name,phone_number=phone_number,
					speciality=speciality,qualification=qualification,location=location,hospital_name=hospital_name,
					doctor_username=doctor_username)
				print('success')
				return HttpResponseRedirect(reverse('doctor_dashboard'))
			except:
				print('not successful :( ')


	return render(request,'basic_app/doctor_dashboard.html',context)

@login_required
def delDocApp(request,pk):

	deldocapp = Appointments.objects.get(id=pk)
	deldocapp.delete()

	return HttpResponseRedirect(reverse('doctor_dashboard'))

def prescription(request,pk):

	appDetails = Appointments.objects.get(id=pk)



	context = {'patientid':pk, 'patientName':(appDetails.First_name+' '+appDetails.Last_name),
	'doctorName':appDetails.doctor,'appdate':appDetails.date,'phone':appDetails.phone_number}

	if request.method == 'POST':

		# appDetails.prescription_status = 'True'
		# appDetails.save()

		context2 = {'symptom':request.POST['symptom'],'medicine':request.POST['medicine'],'doctorFee':request.POST['doctorFee'],'otherCharges':request.POST['otherCharges'],'medicineFee':request.POST['medicineFee'],'total':(int(request.POST['doctorFee'])+int(request.POST['medicineFee'])+int(request.POST['otherCharges']))}
		context.update(context2)

		pres = Prescription()

		pres.patientid=pk
		pres.patient_username = appDetails.patient_username
		pres.patientName = (appDetails.First_name+' '+appDetails.Last_name)
		pres.patientPhone = appDetails.phone_number
		pres.appointmentDate = appDetails.date
		pres.doctorName = appDetails.doctor
		pres.symptom = request.POST['symptom']
		pres.medicine = request.POST['medicine']
		pres.doctorFee = request.POST['doctorFee']
		pres.medicineFee = request.POST['medicineFee']
		pres.otherCharges = request.POST['otherCharges']
		pres.total = (int(request.POST['doctorFee'])+int(request.POST['medicineFee'])+int(request.POST['otherCharges']))
		pres.save()

		message_to_send = request.POST['medicine']
		message_to_send = message_to_send.replace(',','\n')

		send_message(f'Your prescription of medicines is as follows:\n{message_to_send}')

		return render(request,'basic_app/finalprescription.html',context)


	return render(request,'basic_app/prescription.html',context)


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse(pdf,content_type='application/pdf')



def download_pdf_view(request,pk):
    pres= Prescription.objects.filter(patientid=pk).order_by('-id')[:1]
    print(pres)
    dict={
        'patientName':pres[0].patientName,
        'doctorName':pres[0].doctorName,
        'patientPhone':pres[0].patientPhone,
        'appdate':pres[0].appointmentDate,
        'symptom':pres[0].symptom,
        'medicine':pres[0].medicine,
        'medicineFee':pres[0].medicineFee,
        'doctorFee': pres[0].doctorFee,
        'otherCharges':pres[0].otherCharges,
        'total': pres[0].total,
    }
    return render_to_pdf('basic_app/download.html',dict)

def download_patient(request,pk):
    pres= Prescription.objects.get(id=pk)

    print(pres)
    dict={
        'patientName':pres.patientName,
        'doctorName':pres.doctorName,
        'patientPhone':pres.patientPhone,
        'appdate':pres.appointmentDate,
        'symptom':pres.symptom,
        'medicine':pres.medicine,
        'medicineFee':pres.medicineFee,
        'doctorFee': pres.doctorFee,
        'otherCharges':pres.otherCharges,
        'total': pres.total,
    }
    return render_to_pdf('basic_app/download.html',dict)

def download_doctor(request,pk):
    pres= Prescription.objects.get(patientid=pk)

    print(pres)
    dict={
        'patientName':pres.patientName,
        'doctorName':pres.doctorName,
        'patientPhone':pres.patientPhone,
        'appdate':pres.appointmentDate,
        'symptom':pres.symptom,
        'medicine':pres.medicine,
        'medicineFee':pres.medicineFee,
        'doctorFee': pres.doctorFee,
        'otherCharges':pres.otherCharges,
        'total': pres.total,
    }
    return render_to_pdf('basic_app/download.html',dict)



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



    
        
         

	


