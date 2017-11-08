#for basic email
from django.shortcuts import render
from django.core.mail import send_mail

#for attachment email
from django.core.mail import EmailMessage

#for getting the latest file
import glob
import os

#for general report
from datetime import datetime
from Device.models import *

# Create your views here.
from django.http import HttpResponse

#TEST======================================================
from MyGarden.settings import LOG_FILE
def test(request):
	return HttpResponse(LOG_FILE)

# http://192.168.0.69:8000/email/
def index(request):
	mail_return = send_mail('GR summary Jan 31st', 'Activations 1\n Reading 2', 'MyGarden@MyRoom.org', ['paulomariomariomario@gmail.com'])
	return HttpResponse("Email sent!")

# http://192.168.0.69:8000/email/attach
def attach(request):
	email = EmailMessage(
	'Last file test', #subject
	'Body goes here', #body
	'MyGarden@MyHome.com', #from
	['paulomariomariomario@gmail.com'], #to
	#['bcc@example.com'], #bcc
	#reply_to=['other@example.com'],
	#headers={'Message-ID': 'foo'},
	)

	for file_order in [1,6,12]: #newest, 6th newest and 12th newest file
		attachment_file = getLastCreatedFile('/home/pi/webcam/', file_order)
		if (attachment_file != None):
			email.attach_file(attachment_file)
#	email.attach_file('/home/pi/webcam/2017-02-02_0000.jpg')
	email.send()
	return HttpResponse("Email sent!")

# http://192.168.0.69:8000/email/send_update
def send_update(request):
	email = EmailMessage(
	'[GR Report] in '+datetime.now().strftime("%A, %d/%b, %H:%M"), #subject
	getLastReport(), #body
	'MyGarden@MyHome.com', #from
	['paulomariomariomario@gmail.com'], #to
    	#['bcc@example.com'], #bcc
    	#reply_to=['other@example.com'],
	#headers={'Message-ID': 'foo'},
	)

	for file_order in [1,6,12]: #newest, 6th newest and 12th newest file
		attachment_file = getLastCreatedFile('/home/pi/webcam/', file_order)
		if (attachment_file != None):
			email.attach_file(attachment_file)
#	email.attach_file('/home/pi/webcam/2017-02-02_0000.jpg')

	email.send()
	return HttpResponse("Email sent!")

def getLastReport():
	report = ''
	for obj in Device.objects.all():
		report += obj.__str__()+'\n'
		#print only the 150 most recent input results
		for log in obj.getLogs().filter(message__icontains='input').order_by('-log_dt')[:150]:
			report += log.__str__()+'\n'
	report += '\n\n\n'	
	return report

	

def getLastCreatedFile(dir, file_order=1):
	files = glob.glob(dir+'*')
	files.sort(key=os.path.getmtime) #order files
	if len(files)>=file_order:
		return files[len(files)-file_order] #get last (most recent) file
	else:
		return None

