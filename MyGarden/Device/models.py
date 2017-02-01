# import RPi.GPIO as GPIO
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


def populateDefaultDevices():
	sk1_hygro = Device(name='SK1 Hygrometer', type='SENSOR', subtype='HYGROMETER', gpio_pin=17)
	sk2_hygro = Device(name='SK2 Hygrometer', type='SENSOR', subtype='HYGROMETER', gpio_pin=22)
	sk1_pump = Device(name='SK1 Water Pump', type='ACTUATOR', subtype='PUMP', gpio_pin=23, 						activation_mode='FIXED')
	sk2_pump = Device(name='SK2 Water Pump', type='ACTUATOR', subtype='PUMP', gpio_pin=24, 						activation_mode='FIXED')
	gr_light = Device(name='GR Lights', type='ACTUATOR', subtype='LIGHT', gpio_pin=4, 						activation_mode='FIXED')
	sk1_hygro.save()
	sk2_hygro.save()
	sk1_pump.save()
	sk2_pump.save()
	gr_light.save()

# Create your models here.
class Device(models.Model):
	name = models.CharField(max_length=20, default=None, blank=True, null=True) 		
	type = models.CharField(max_length=10) 			#Either SENSOR or ACTUATOR
	subtype = models.CharField(max_length=10) 		#Either LIGHT, PUMP, or HYGROMETER
	gpio_pin = models.IntegerField(null=True)		#Raspberry Pi control pin
	potency = models.DecimalField(decimal_places = 2, max_digits = 8, null=True) #For the actuators
	potency_unit = models.CharField(max_length=32, null=True) 	#For the actuators
	activation_mode = models.CharField(max_length=32, null=True) 	#For the actuators. Either FIXED or DYNAMIC

	#Avoid coersion errors
#	def __unicode__(self):
#		return unicode(self.some_field) or u''

	def __str__(self):
#		return self.name +'('+self.subtype+'/'+self.activation_mode+')'
		return self.name

	def logEvent(self, msg=''):
		mylog = DeviceLog(device_id=self.id, message_dt=timezone.now(), message=msg)
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
		return '['+str(self.log_dt)+'] ['+self.device.__str__()+'] ['+self.message+']'

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


