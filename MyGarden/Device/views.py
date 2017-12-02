#File in /home/pi/git/growroom/MyGarden/Device

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from Device.models import *
from datetime import datetime

def index(request):
	# print('lalal1')
	# return HttpResponse('yo mann')
	
    mystr = ''
    for cur_device in Device.objects.all():
    	cur_device.logEvent('breakpoint1 '+str(datetime.now()))
    	print('breakpoint1 '+str(datetime.now()))
    
    for cur_device in Device.objects.all():
    	for cur_log in cur_device.getLogs():
    		print('breakpoint2 '+cur_log.__str__())
    		mystr += 'breakpoint2 ' + cur_log.__str__() + '\n'

    return HttpResponse(mystr)
    # return HttpResponse("Hello, world. You're at the DEVICE index.")

def update_all(request):
	#process sensors
	for sensor in Device.objects.all():
		sensor.update()

	return HttpResponse("Finished updating all devices!")
