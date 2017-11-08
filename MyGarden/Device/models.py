#File location: /home/pi/git/growroom/MyGarden/Device

import sys
import RPi.GPIO as GPIO
import time
#from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from MyGarden.settings import LOG_FILE
from datetime import datetime


def populateDefaultDevices():
	for obj in Device.objects.all(): obj.delete()
	#Device.objects.all().delete()
	sk1_hygro = Device(name='SK1 Hygrometer', type='SENSOR', subtype='HYGROMETER', gpio_pin=17)
	sk2_hygro = Device(name='SK2 Hygrometer', type='SENSOR', subtype='HYGROMETER', gpio_pin=22)
	#sk1_pump = Device(name='SK1 Water Pump', type='ACTUATOR', subtype='PUMP', gpio_pin=23, activation_mode='FIXED', activation_duration=7.1, activation_dose = '100 ml with a 14.1 ml/sec pump', activation_frequency=3600*24)
	#sk2_pump = Device(name='SK2 Water Pump', type='ACTUATOR', subtype='PUMP', gpio_pin=24,	activation_mode='FIXED', activation_duration=1.7, activation_dose = '50ml with a 29.6ml/s pump', activation_frequency=3600*36)
#	gr_light = Device(name='GR Lights', type='ACTUATOR', subtype='LIGHT', gpio_pin=4, activation_mode='FIXED', activation_duration=20, activation_frequency=40)
	sk1_hygro.save()
	sk2_hygro.save()
#	sk1_pump.save()
#	sk2_pump.save()
#	gr_light.save()

# Create your models here.
class Device(models.Model):
	name = models.CharField(max_length=20, default=None, blank=True, null=True) 		
	type = models.CharField(max_length=10) 			#Either SENSOR or ACTUATOR
	subtype = models.CharField(max_length=10) 		#Either LIGHT, PUMP, or HYGROMETER
	gpio_pin = models.IntegerField(null=True)		#Raspberry Pi control pin
	
	potency = models.DecimalField(decimal_places = 2, max_digits = 8, null=True) #For the actuators	
	potency_unit = models.CharField(max_length=32, null=True) 	#For the actuators
	activation_status = models.CharField(max_length=32, null=True) #For the actuators. Either ACTIVE or INACTIVE
	activation_mode = models.CharField(max_length=32, null=True) 	#For the actuators. Either FIXED or DYNAMIC
	activation_duration = models.DecimalField(decimal_places = 2, max_digits = 8, null=True) #[in seconds] ACTUATORS ONLY. How long it should be active for
	activation_dose = models.CharField(max_length = 32, null=True) #[units description] ACTUATORS ONLY. The measuring units corresponding to the activation_duration
	activation_frequency = models.DecimalField(decimal_places = 2, max_digits = 8, null=True) #[in seconds] ACTUATORS ONLY activation frequency
	last_activation = models.DateTimeField(null=True)
	#min_idle_time = models.DecimalField(decimal_places = 2, max_digits = 8, null=True) #[in seconds] ACTUATORS ONLY. Min time between activations

	def __str__(self):
		return self.name

	def fullStr(self):
		str = '[name: '+self.name+'] ' 
		str += ('[type: '+self.type+'] ' if self.type!=None else '')
		str += ('[subtype: '+self.subtype+'] ' if self.subtype!=None else '') 
		str += ('[gpio_pin: '+str(self.gpio_pin)+'] ' if self.gpio_pin!=None else '')
		return str

	def update(self):
		GPIO.setmode(GPIO.BCM)

		if self.type=='ACTUATOR':
			GPIO.setup(self.gpio_pin, GPIO.OUT)

			last_activation_endtime =   self.last_activation + timedelta(seconds=self.activation_duration)
			next_activation_starttime = self.last_activation + timedelta(seconds=self.activation_frequency)
			now = datetime.now()

			#check if ACTUATOR should be activated or deactivated
			if self.last_activation==None:
				#ACTIVATE FOR THE 1ST TIME
				self.logEvent('to be activated - 1st time')
				GPIO.output(self.gpio_pin, True)
				self.logEvent('after activation attempt - 1st time')
	
				self.activation_status = 'ACTIVE'
				self.last_activation = now				

			elif last_activation_endtime < now or next_activation_starttime < now:
				#ACTIVATE
				self.logEvent('pre activation')
				GPIO.output(self.gpio_pin, True)
				self.logEvent('after activation attempt')
				
				#Check if status needs to be changed (Activation in 1st refresh after inactive time)
				if self.activation_status=='INACTIVE': #equivalent to next_activation_start_time < now
					self.logEvent('changing status from INACTIVE to ACTIVE')
					self_activation_status = 'ACTIVE'
					self.last_activation = now
				
				#process short events (<60s) imediatelly
				if self.activation_duration<60:
					sleep(self.activation_duration)
					#deactivate
					GPIO.output(self.gpio_pin, False) 
					self.activation_status = 'INACTIVE'
				
			elif  last_activation_endtime >= now:
				#DEACTIVATE
				self.logEvent('to be (kept) deactivated')
				GPIO.output(self.gpio_pin, False)
				self.logEvent('after (keeping) deactivation attempt')

				self.activation_status = 'INACTIVE'
			
			self.save()						
		elif self.type == 'SENSOR':
			GPIO.setup(self.gpio_pin, GPIO.IN)
#			self.logEvent('Before reading')
			input = GPIO.input(self.gpio_pin)
			if input==1: status = 'DRY'
			elif input==0: status = 'WET'
			else: status = 'UNKNOWN:'+str(input)
			self.logEvent('Input='+status)
			
	def logEvent(self, msg='', log_db = True, log_file = True):
		#raw log
		if log_file == True :
			try:
				f=open(LOG_FILE, 'a')
				f.write('['+datetime.now()+'] ['+self.__str__()+'] ['+msg+']\n')
				f.close()
			except:
				self.logEvent("Unexpected error:"+str(sys.exc_info()[0]), True, False)
		
		#DB log
		if log_db == True:
			mylog = DeviceLog(device_id=self.id, log_dt=timezone.now(), message=msg)		
			mylog.save()

	def getLogs(self):
		my_logs = DeviceLog.objects.filter(device_id = self.id)
		return my_logs

	def scheduleEvent(self, event_dt, activation=None):
		myevent = DeviceEvent(device_id=self.id, event_dt=event_dt, activation=activation)
		myevent.save()	

	def getScheduledEvents(self):
		myevents = DeviceEvent.objects.filter(device_id=self.id)
		return myevents;


class DeviceLog(models.Model):
	device = models.ForeignKey(Device, on_delete = models.CASCADE)
	log_dt = models.DateTimeField()
	message = models.CharField(max_length=100)

	def __str__(self):
		formatted_date_time = self.log_dt.strftime("%A, %d/%b, %H:%M:%S") # the format is "Wednesday, 08/Nov, 02:00:02"
		
		return '['+formatted_date_time+'] ['+self.device.__str__()+'] ['+self.message+']'

	class Meta:
		ordering = ('log_dt',)

class DeviceEvent(models.Model):
	device = models.ForeignKey(Device, on_delete = models.CASCADE)
	event_dt = models.DateTimeField()
	activation = models.IntegerField(null=True) #Just for ACTUATORS. Either 1 (activate) or 0 (deactivate) 

	def __str__(self):
		return '['+str(self.event_dt)+'] ['+('ACTIVATE' if self.activation==1 else 'DEACTIVATE')+'] ['+self.device.__str__()+']'

	class Meta:
		ordering = ('event_dt',)


