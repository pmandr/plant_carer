#File in /home/pi/git/growroom/MyGarden/Device

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from Device.models import *
from datetime import datetime

def index(request):
    mystr = ''
    for cur_device in Device.objects.all():
    	cur_device.logEvent('Hello World'+str(datetime.now()))
    return HttpResponse('str'+str(datetime.now()))
    # return HttpResponse("Hello, world. You're at the DEVICE index.")

def update_all(request):
	#process sensors
	for sensor in Device.objects.all():
		sensor.update()

	return HttpResponse("Finished updating all devices!")
