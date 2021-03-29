from django.urls import path
from . import views

urlpatterns = [
    path('',views.front, name = 'front'),
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
    
]
