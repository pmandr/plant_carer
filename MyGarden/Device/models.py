from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Device(models.Model):
	type = models.CharField(max_length=10) 			#Either SENSOR or ACTUATOR
	subtype = models.CharField(max_length=10) 		#Either LIGHT, PUMP, or HYGROMETER
	gpio_pin = models.IntegerField()			#Raspberry Pi control pin
	potency = models.DecimalField(decimal_places = 2, max_digits = 8) 			#For the actuators
	potency_unit = models.CharField(max_length=32)		#For the actuators
	activation_mode = models.CharField(max_length=32) 	#For the actuators. Either SCHEDULED or INTELLIGENT
