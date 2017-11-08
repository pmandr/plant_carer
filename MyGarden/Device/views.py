from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from Device.models import *

def index(request):
    return HttpResponse("Hello, world. You're at the DEVICE index.")

def update_all(request):
	#process sensors
	for sensor in Device.objects.all():
		sensor.update()

	return HttpResponse("Finished updating all devices!")
