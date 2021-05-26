from time import timezone

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.mail import EmailMessage
from django.views.decorators import csrf
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm

from . import forms,models
from .forms import *
import pandas as pd
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.forms import PasswordChangeForm
from .models import Query,Querystatus,Save_value

from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def customer_signup_view(request):
    userForm=CustomerUserForm()
    customerForm=CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=CustomerUserForm(request.POST)
        customerForm=CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='NEW_USER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'customersignup.html',context=mydict)

def is_consellor(user):
    return user.groups.filter(name='CONSELLOR').exists()
def is_newuser(user):
    return user.groups.filter(name='NEW_USER').exists()
def is_admin(user):
    return user.groups.filter(name='G_ADMIN').exists()


def consellorlist(request):
    g_admins = User.objects.filter(groups__name='CONSELLOR')

    if request.method == 'POST':
        var = request.POST.get('assign')
        consellor_id = request.POST.get('val')
        Query.objects.filter(sno = consellor_id).update(assign=var)
    query = Query.objects.all()

    for q in query:
        subject = "query"
        message = f'Hi ,you are getting query from  { request.user.username}.Category Type: { q.category_type} Details: {q.details} Status  : {q.status}'
        email_from = settings.EMAIL_HOST_USER
        for i in g_admins:
            recipient_list = [i.email]
            send_mail(subject, message, email_from, recipient_list)
    return render(request,"view_consellor.html",{"query":query,"consellor":g_admins})



def afterlogin_view(request):
    if is_consellor(request.user):
        return redirect('/consellor-dashboard')
    elif is_newuser(request.user):
        return redirect('/')
    elif is_admin(request.user):
        return redirect('/admin-dashboard')
    else:
        return redirect('/admin')

def consellor_dash(request):
    all =Query.objects.filter(assign=request.user)
    print("--all--",all)
    return render(request,"consellor_dashboard.html",{"all":all})



def admin_user_request(request):
    current_logged_user = User.objects.get(username=request.user.username)
    all_mess=Message.objects.filter(sender__groups__name="NEW_USER",thread__users=current_logged_user)
    all_messages=[msg for msg in all_mess]
    all_assigned_messages=[ass_msg.Message_Id for ass_msg in Messages_Assigned.objects.filter(Assigned_By=request.user.id)]
    ass_msgs_counter=0
    for ass_msgs in all_assigned_messages:
        if ass_msgs in all_messages:
            ind=all_messages.index(ass_msgs)
            all_messages.pop(ind)
        ass_msgs_counter+=1
    all_councellor=User.objects.filter(groups__name="CONSELLOR")
    return render(request, "admin_user_requests.html",{'all_messages':all_messages,"all_councellor":all_councellor,
                                                       "assigned_messages":Messages_Assigned.objects.filter(Assigned_By=request.user.id)})


def assign_msg_request(request):
    #print()
    # print(request.POST.get('message_id'))
    Messages_Assigned(Message_Id=Message.objects.get(id=request.POST.get('message_id')),Assigned=True,Assigned_To=User.objects.get(id=request.POST.get('assigned_to')),
                      Assigned_By=User.objects.get(id=request.user.id),).save()
    return redirect('msgreq-admin')


def redirect_chat(request):
    current_logged_user = User.objects.get(username=request.user.username)

    msg_assigned_users=Messages_Assigned.objects.filter(Assigned_To=current_logged_user)

    all_users=[users.Message_Id.sender for users in msg_assigned_users]

    # if group_type == 'CONSELLOR' or group_type == "G_ADMIN":
    #     print("IS CONSELLOR or GADMIN")
    #     all_users = User.objects.all().exclude(username=request.user.username)
    #     print(all_users)
    return render(request, "mychats.html", {'all_users': all_users})



def messagereqcoun(request):
    print(request.user.id)
    return render(request, "councellor_msg_req.html",{"assigned_messages":Messages_Assigned.objects.filter(Assigned_To=request.user.id)})


def deletemsg(request):
    Message.objects.get(id=request.GET.get("msg_id")).delete()
    return redirect('msgreq-admin')


###############-----------------Admin Dashboard-------######################
@login_required(login_url='customerlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):   #main page views
    # for cards on dashboard
    customercount=Customer.objects.all().count()
    hospitalcount=Hospital.objects.all().count()
    bankcount=Bank.objects.all().count()
    query = Querystatus.objects.all()

    for querys in query:
        print("-----",querys.status)

    mydict={
    'customercount':customercount,
    'hospitalcount':hospitalcount,
    'bankcount':bankcount,
     'status':""
    }
    return render(request,'admin_dashboard.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def view_customer_view(request):
    customers=Customer.objects.all()
    return render(request,'view_customer.html',{'customers':customers})
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_customer(request):
    userForm=CustomerUserForm()
    customerForm=CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=CustomerUserForm(request.POST)
        customerForm=CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='NEW_USER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/view-customer')
    return render(request,'admin_add_users.html',context=mydict)
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_customer(request,pk):
    customer=Customer.objects.get(id=pk)
    customer.delete()
    return redirect('/view-customer')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_hospital(request):
    hospitals= Hospital.objects.all()
    return render(request,"admin_hospitals.html",{"hospitals":hospitals})
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def add_hospital(request):
    hospitalForm=HospitalForm()
    if request.method=='POST':
        hospitalForm=HospitalForm(request.POST, request.FILES)
        if hospitalForm.is_valid():
            hospitalForm.save()
        return HttpResponseRedirect('admin-hospital')
    return render(request,'admin_add_hospitals.html',{'hospitalForm':hospitalForm})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_hospital(request,pk):
    hospital=Hospital.objects.get(id=pk)
    hospital.delete()
    return redirect('/admin-hospital')
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_bank(request):
    banks= Bank.objects.all()
    return render(request,"admin_banks.html",{"banks":banks})
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def add_bank(request):
    bankForm=BankForm()
    if request.method=='POST':
        bankForm=BankForm(request.POST, request.FILES)
        if bankForm.is_valid():
            bankForm.save()
        return HttpResponseRedirect('admin-bank')
    return render(request,'admin_add_banks.html',{'bankForm':bankForm})
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_bank(request,pk):
    bank=Bank.objects.get(id=pk)
    bank.delete()
    return redirect('/admin-bank')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_gp(request):
    gps= Gp.objects.all()
    return render(request,"admin_gps.html",{"gps":gps})
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def add_gp(request):
    gpForm=GpForm()
    if request.method=='POST':
        gpForm=GpForm(request.POST, request.FILES)
        if gpForm.is_valid():
            gpForm.save()
        return HttpResponseRedirect('admin-gp')
    return render(request,'admin_add_gp.html',{'gpForm':gpForm})
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_gp(request,pk):
    gp=Gp.objects.get(id=pk)
    gp.delete()
    return redirect('/admin-gp')
def admin_contactus(request):
    contact= ContactUs.objects.all()
    return render(request,"admin_contact.html",{"contact":contact})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_asy(request):
    asy= Assylum.objects.all()
    return render(request,"admin_asy.html",{"asy":asy})
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def add_asy(request):
    asyForm=AsyForm()
    if request.method=='POST':
        asyForm=AsyForm(request.POST, request.FILES)
        if asyForm.is_valid():
            asyForm.save()
        return HttpResponseRedirect('admin-asy')
    return render(request,'admin_add_asy.html',{'asyForm':asyForm})
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_asy(request,pk):
    asy=Assylum.objects.get(id=pk)
    asy.delete()
    return redirect('/admin-asy')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_ref(request):
    ref= Refuse.objects.all()
    return render(request,"admin_ref.html",{"ref":ref})
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def add_ref(request):
    refForm=RefForm()
    if request.method=='POST':
        refForm=RefForm(request.POST, request.FILES)
        if refForm.is_valid():
            refForm.save()
        return HttpResponseRedirect('admin-ref')
    return render(request,'admin_add_ref.html',{'refForm':refForm})
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_ref(request,pk):
    ref=Refuse.objects.get(id=pk)
    ref.delete()
    return redirect('/admin-ref')


#############------------------End Admin View--------########################





def front(request):
    wel =WelcomeNotes.objects.all()
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/contactus')
    else:
        form = Contact()

    return render(request, 'Main.html',{"form":form,"welcome":wel})

def publicservices(request):
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    return render(request,'publicservices.html',{"form":form})


def healthservices(request):
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    return render(request,'HealthServices.html',{"form":form})

def hospitals(request):
    dests = Hospital.objects.all()
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    return render(request, 'HospitalsNear.html', {'dests': dests,"form":form})

def gp(request):
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    return render(request, 'GP.html',{"form":form})

def banks(request):
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    banks = Bank.objects.all()
    return render(request, 'banks.html', {'banks' : banks,"form":form})

def gp(request):
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    banks = Gp.objects.all()
    return render(request, 'GP.html', {'banks' : banks,"form":form})

def transport(request):
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    return render(request, 'Transport.html',{"form":form})

def emergency(request):
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    return render(request, 'Emergency.html',{"form":form})

def localservices(request):
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    return render(request,'LocalServices.html',{"form":form})

def refugee(request):
    refe = Refuse.objects.all()
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    return render(request, 'Refugee.html',{"form":form, 'refe':refe})

def assylumseeker(request):
    helps =  Assylum.objects.all()
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    return render(request, 'AssylumSeeker.html', {'helps' : helps,"form":form})

def base(request):
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    return render(request, 'base.html',{"form":form})

def login(request):
    return render(request, 'login.html')

def contactus(request):
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    return render(request, 'contact.html', {'form': form})
def contactusapi(request):
    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/')
    else:
        form = Contact()
    return render(request, 'contactusapi.html', {'form': form})
@login_required(login_url='customerlogin')
@user_passes_test(is_newuser)
def chat(request):
    return render(request,"chat.html")


def change_password(request):
    if request.method== "POST":
        form = PasswordChangeForm(data= request.POST,user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('profiledashboard')
        else:
            return redirect('change_password')

    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
    return render(request, 'change_password.html', args)


def profile_dashboard(request):
     return render(request,"dashboard.html")


def Queryform(request):
    if request.method == "POST":
        form = QueryForm(request.POST)

        if form.is_valid():
            query = form.save(commit=False)
            query.user =request.user
            query.save()
            return redirect('/')
    form = QueryForm()
    return render(request, "queryform.html",{"form":form})


def Querystatusform(request,pk):
    query = get_object_or_404(Query, pk=pk)
    print("---query----",query)
    if request.method == "POST":
        form = QueryStatus(request.POST, instance=query)
        if form.is_valid():
            query = form.save(commit=False)
            query.user = request.user
            query.save()
            return redirect('view-consellor')
    else:
        form = QueryStatus(instance=query)
    return render(request, 'editstatus.html', {'form': form})


def delete_query(request,pk):
    ref=Query.objects.get(id=pk)
    ref.delete()
    return redirect('/view-consellor')

def viewquery(request):
    all = Query.objects.all()
    for i in all:
        print("value",i.status)


    return render(request,"viewquery.html",{"all":all})

def editquery(request,pk):
    query = get_object_or_404(Query, pk=pk)
    if request.method == "POST":
        form = QueryForm(request.POST, instance=query)
        if form.is_valid():
            query = form.save(commit=False)
            query.user = request.user

            query.save()
            return redirect('view-query')
    else:
        form = QueryForm(instance=query)
    return render(request, 'editquery.html', {'form': form})


def userdelete_query(request,pk):
    ref=Query.objects.get(sno=pk)
    ref.delete()
    return redirect('/view-query')


def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("view-profile")
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'edit_profile.html', args)


















