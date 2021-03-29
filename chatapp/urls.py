from django.urls import path,re_path

from . import views

urlpatterns = [
    path('', views.chatapp, name='chatapp'),
      path('<str:room_name>/', views.room, name='room'),
]