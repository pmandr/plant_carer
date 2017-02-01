from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.
from django.http import HttpResponse

def index(request):
#	send_mail('ASSUNTO TESTE', 'MSG TESTE', 'buffalosoldierbr@hotmail.com', 'paulomariomariomario@gmail.com')
#	return HttpResponse("Hello World. This is my email app")
	mail_return = send_mail('GR summary Jan 31st', 'Activations 1\n Reading 2', 'MyGarden@MyRoom.org', ['paulomariomariomario@gmail.com'])
	return HttpResponse("Email sent!")

