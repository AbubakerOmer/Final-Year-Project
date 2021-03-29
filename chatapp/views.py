from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
# Create your views here.
def chatapp(request):
    return render(request, 'chat.html')

def room(request, room_name):
    return render(request, 'room.html',{'room_name': room_name})