from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Hospital, Records
# Create your views here.
import pyrebase

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
            return HttpResponse("<h1>Login Credentials are incorrect</h1>")
    return render(request, "Hospital/firstpage.html")


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
    for i in range(10):
        patient_name = request.POST.get('patient_name' + str(i))
        contact = request.POST.get('contact_no' + str(i))
        addr = request.POST.get('addr' + str(i))
        doctor = request.POST.get('doctor_name' + str(i))
        token = request.POST.get('token_no' + str(i))
        checked_out = request.POST.get('checked_out' + str(i))
        type1 = request.POST.get('type1' + str(i))
        type2 = request.POST.get('type2' + str(i))
        type3 = request.POST.get('type3' + str(i))
        rc = Records.objects.filter(patient_name=patient_name)
        print(rc)
        if rc is not None:
            for r in rc:
                r.Doctor_attending = doctor
                r.Appointment_no = token
                r.is_checked_out = checked_out
                r.type1 = type1
                r.type2 = type2
                r.type3 = type3
                r.save()

        calculate_beds(request, h)
        calculate_app_no(request, h)
    return render(request, "Hospital/excel(1).html", {'records': record})


def create():
    print("hello")


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
        global h_name
        h_name = name
    return render(request, "Hospital/Register.html", {'h_name': h_name})


@csrf_exempt
def appointment(request, string):
    hospital = Hospital.objects.get(name=string)
    doctors =hospital.doctors_set.all()
    if request.POST:
        a = request.POST['slots']
        if a == '9-10':
            print("hello")
    return render(request, "Hospital/appointment.html", {'doctors': doctors})