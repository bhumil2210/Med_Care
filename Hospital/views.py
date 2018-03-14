from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login as auth,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Hospital,Doctors,Timing
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
def excel(request):
    return render(request, "Hospital/list_hospital.html")


@csrf_exempt
def register(request):
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
    return render(request, "Hospital/Register.html")


@csrf_exempt
def appointment(request, string):
    hospital = Hospital.objects.get(name=string)
    doctors =hospital.doctors_set.all()
    if request.POST:
        a = request.POST['slots']
        if a == '9-10':
            print("hello")
    return render(request, "Hospital/appointment.html", {'doctors': doctors})