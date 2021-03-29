from django.shortcuts import render
from .models import Hospital, Bank, AssylumHelp


# Create your views here.
def front(request):
    return render(request,'Main.html')

def publicservices(request):
    return render(request,'publicservices.html')


def healthservices(request):
    return render(request,'HealthServices.html')

def hospitals(request):
    dests = Hospital.objects.all() 
    return render(request, 'HospitalsNear.html', {'dests': dests})

def gp(request):
    return render(request, 'GP.html')

def banks(request):
    banks = Bank.objects.all()
    return render(request, 'banks.html', {'banks' : banks})

def transport(request):
    return render(request, 'Transport.html')

def emergency(request):
    return render(request, 'Emergency.html')

def localservices(request):
    return render(request,'LocalServices.html')

def refugee(request):
    return render(request, 'Refugee.html')

def assylumseeker(request):
    helps =  Bank.objects.all()
    return render(request, 'AssylumSeeker.html', {'helps' : helps}) 

def base(request):
    return render(request, 'base.html')

def login(request):
    return render(request, 'login.html')

