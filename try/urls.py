"""try URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from app import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.front, name = 'front'),
    path('contactus/', views.contactus, name='contact-us'),
    path('admin-dashboard/',views.admin_dashboard_view,name="admin"),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='Main.html'),name='logout'),
    path('adminlogin', LoginView.as_view(template_name='adminlogin.html'),name='adminlogin'),


    path('customersignup', views.customer_signup_view),
    path('customerlogin', LoginView.as_view(template_name='customerlogin.html'),name='customerlogin'),
    path('password-reset/',auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             success_url='/password-reset/done/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    # path('accounts/', include('django.contrib.auth.urls')),





    path('view-customer', views.view_customer_view,name='view-customer'),
    path('add-customer', views.admin_add_customer,name='add-customer'),
    path('admin-hospital',views.admin_hospital,name="admin-hospital"),
    path('add-hospital', views.add_hospital,name='add-hospital'),
    path('admin-bank',views.admin_bank,name="admin-bank"),
    path('add-bank', views.add_bank,name='add-bank'),
    path('admin-gp',views.admin_gp,name="admin-gp"),
    path('admin-asy',views.admin_asy,name="admin-asy"),
    path('admin-ref',views.admin_ref,name="admin-ref"),
    path('add-asy',views.add_asy,name="add-asy"),
    path('add-ref',views.add_ref,name="add-ref"),
    path('add-gp', views.add_gp,name='add-gp'),
    path('delete-customer/<int:pk>', views.delete_hospital,name='delete-customer'),
    path('admin-contact',views.admin_contactus,name="con-admin"),
    path('delete-hospital/<int:pk>', views.delete_hospital,name='delete-hospital'),
    path('delete-asy/<int:pk>', views.delete_asy,name='delete-asy'),
    path('delete-ref/<int:pk>', views.delete_ref,name='delete-ref'),
    path('delete-bank/<int:pk>', views.delete_bank,name='delete-bank'),
    path('delete-gp/<int:pk>', views.delete_gp,name='delete-gp'),
    path('publicservices',views.publicservices,  name = "publicservices"),
    path('healthservices',views.healthservices, name = "healthservices"),
    path('hospitals', views.hospitals, name  = "hospitals"),
    path('gp', views.gp, name = "gp"),
    path('banks', views.banks, name = "banks"),
    path('transport', views.transport, name = "transport"),
    path('emergency', views.emergency, name = "emergency"),
    path('localservices', views.localservices, name =  "localservices"),
    path('assylumseeker', views.assylumseeker, name = "assylumseeker"),
    path('refugee', views.refugee, name = "refugee"),
    path('base', views.base, name = "base"),
    # path('chat/',views.chat,name="chat"),
    path('gp/',views.gp),
    path('profiledashboard/', views.profile_dashboard,name="profiledashboard"),
    path('change_password/', views.change_password, name='change_password'),
    path('view-consellor/', views.consellorlist, name='view-consellor'),
    path('consellor-dashboard/', views.consellor_dash, name='consellor-dashboard'),
    path('messagereqcoun/', views.messagereqcoun, name='messagereqcoun'),
    path('deletemsg/',views.deletemsg,name="deletemsg"),
    path('admin-user-request', views.admin_user_request, name="msgreq-admin"),
    path('assign-msg-request', views.assign_msg_request, name="assign-msg-request"),
    path('redirect_chat/',views.redirect_chat,name="redirect_chat"),


    path('query-form/', views.Queryform, name='query-form'),
    path('query-status/', views.Querystatusform, name='query-status'),
    path('delete-query/<int:pk>', views.delete_query, name='delete-query'),
    path('edit-query/<int:pk>/', views.editquery, name='edit-query'),
    path('view-query', views.viewquery, name='view-query'),
    path('userdelete-query/<int:pk>', views.userdelete_query, name='userdelete-query'),
    path('edit-querystatus/<int:pk>/', views.Querystatusform, name='edit-querystatus'),
    path('view-profile', views.view_profile, name='view-profile'),
    path('edit-profile', views.edit_profile, name='edit-profile'),


    path('chat/',include("chat.urls"))


]
