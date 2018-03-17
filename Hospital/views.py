import datetime

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Hospital, Records,Doctors,Medicine
# Create your views here.
import pyrebase
import infermedica_api
import json

config = {
    "apiKey": "AIzaSyDHI0IQj0PsLk-xUSOpHGSJvUUT0rgzsas",
    "authDomain": "medcare-4ade6.firebaseapp.com",
    "databaseURL": "https://medcare-4ade6.firebaseio.com",
    "projectId": "medcare-4ade6",
    "storageBucket": "",
    "messagingSenderId": "208246513043"
  }
firebase = pyrebase.initialize_app(config)

@csrf_exempt
def login(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                auth(request, user)
                return redirect('/dashboard/')
        else:
            return redirect('/excel/'+username)
    return render(request, "Hospital/firstpage.html", {'username': username})


@login_required(login_url='/login/')
def dashboard(request):
    return render(request, "Hospital/dashboard.html")


@csrf_exempt
def list_hospital(request):
    query_set = Hospital.objects.all()
    q = request.GET.get("filter")
    if q:
        query_set = query_set.filter(
            Q(name__icontains=q) |
            Q(type1__icontains=q) |
            Q(type2__icontains=q) |
            Q(type3__icontains=q) |
            Q(city__icontains=q) |
            Q(state__icontains=q)
        )
    return render(request, "Hospital/list_hospital.html", {'query_set': query_set})


@csrf_exempt
def excel(request, string):
    h = Hospital.objects.get(name=string)
    record = h.records_set.all()
    d = h.doctors_set.all()
    i=0
    for i in range(10):
        patient_name = request.POST.get('patient_name' + str(i))
        contact = request.POST.get('contact_no' + str(i))
        addr = request.POST.get('addr' + str(i))
        doctor = request.POST.get('doctor_name' + str(i))
        speciality = request.POST.get('specialist'+str(i))
        type1 = request.POST.get('type1' + str(i))
        type2 = request.POST.get('type2' + str(i))
        type3 = request.POST.get('type3' + str(i))
        rc = Records.objects.filter(patient_name=patient_name, hospital=h)
        """" if not rc and patient_name is not None:
            print("hello")
            create(h,patient_name,contact,addr,doctor,speciality,type1,type2,type3)"""
        if check(rc):
            for r in rc:
                r.Doctor_attending = doctor
                r.speciality = speciality
                r.type1 = type1
                r.type2 = type2
                r.type3 = type3
                r.save()
        """elif check(rc) is False:
            print("hello")
            create(h, patient_name, contact, addr, doctor, speciality, type1, type2, type3)"""
        if request.method == 'POST' and 'btn2' in request.POST:
            for j in range(10):
                d_name = request.POST.get('name' + str(j))
                current_no = request.POST.get('current' + str(j))
                last = request.POST.get('last' + str(j))
                d_o = Doctors.objects.filter(name=d_name, Hospital=h)
                if d_o:
                    for d in d_o:
                        d.current_app_no = current_no
                        d.assigned_app_no = last
                        d.save()
        calculate_beds(request, h)
        #calculate_app_no(request, h)
    return render(request, "Hospital/excel(1).html", {'records': record, 'doctor': d, 'h': h})


def check(rc):
    if rc:
        return True
    else:
        return False


def create(h,patient_name,contact,addr,doctor,speciality,type1,type2,type3):
    Records.objects.create(hospital=h,patient_name=patient_name,contact_no=contact,Address=addr,Doctor_attending=doctor,speciality=speciality,type1=type1,type2=type2,type3=type3)


def calculate_app_no(request, h):
    doctors = h.doctors_set.all()
    for doctor in doctors:
        if doctor:
            r = Records.objects.filter(Doctor_attending=doctor.name)
            s = r.last()
            doctor.app_no = s.Appointment_no
            doctor.save()
        else:
            pass


@csrf_exempt
def calculate_beds(request, h):
    bed1 = Records.objects.filter(type1='Y',hospital=h).count()
    bed2 = Records.objects.filter(type2='Y',hospital=h).count()
    bed3 = Records.objects.filter(type3='Y',hospital=h).count()
    h.no_of_beds_available = int(int(h.total_beds) - int(bed1) - int(bed2) - int(bed3))
    h.type1 = int(bed1)
    h.type2 = int(bed2)
    h.type3 = int(bed3)
    h.save()


@csrf_exempt
def register(request):
    h_name = ""
    if request.POST:
        name = request.POST['name']
        Address1 = request.POST['Address1']
        Address2 = request.POST['Address2']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        lt = Hospital.objects.create(
            name=name,
            Address1=Address1,
            Address2=Address2,
            city=city,
            state=state,
            zip_code=zip)
        lt.save()
        #global h_name
        #h_name = name
    return render(request, "Hospital/Register.html")


@csrf_exempt
def appointment(request, string):
    hospital = Hospital.objects.get(name=string)
    doctors = hospital.doctors_set.all()
    for doctor in doctors:
        if request.POST.get('btn' + str(doctor.name)):
            print("hello")
            current = doctor.current_app_no
            last = doctor.assigned_app_no
            time = str(datetime.datetime.now())
            expected_time = int(last) - int(current)
            redirect("Hospital/app.html", expected_time, current, last)
    return render(request, "Hospital/appointment.html", {'doctors': doctors})


@csrf_exempt
def symp_checker(request):
    text = text1 = text2 = text3 = condition = ""
    if request.method == 'POST' and 'btn' in request.POST:
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        symptons = request.POST.get("symptons")
        print(symptons)
        api = infermedica_api.API(app_id='5e56236e', app_key='ab1d0c08bf4a8d96e23eb00918f211cb')
        r = api.parse(symptons)
        j = json.loads(str(r))
        d = infermedica_api.Diagnosis(gender, age)
        for i in range(len(j['mentions'])):
            d.add_symptom(j['mentions'][i]['id'], j['mentions'][i]['choice_id'], initial=True)

        d = api.diagnosis(d)
        text = d.question.text
        print(text)
        if request.POST.get("present1"):
            d.add_symptom(d.question.items[0]['id'], d.question.items[0]['choices'][1]['id'])
            d = api.diagnosis(d)
            text1 = d.question.text
        if request.POST.get("present2"):
            d.add_symptom(d.question.items[0]['id'], d.question.items[0]['choices'][1]['id'])
            d = api.diagnosis(d)
            text2 = d.question.text

        condition = d.conditions[0]['name']
    return render(request,"Hospital/sympton.html",{'text':text, 'text1':text1, 'text2':text2, 'condition':condition})


def location(request,string):
    return render(request, "Hospital/location.html", {'string':string})


def order_medicine(request):
    m = Medicine.objects.all().order_by('price')
    q = request.GET.get('search')
    if q:
        m = Medicine.objects.filter(
            Q(location__icontains=q) |
            Q(name__icontains=q)
        )
    return render(request,"Hospital/om.html",{'m': m})
