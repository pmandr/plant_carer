import RPi.GPIO as GPIO
from sys_config import sys_config
import time

# Set our GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

class Actuator:

	def __init__(self, in_GPIO_pin, in_type, in_activation_time = 0):
		self.v_GPIO_pin = in_GPIO_pin
		self.v_type = in_type
		self.v_activation_time = in_activation_time
		self.v_active = True

		# Set the GPIO pin to an input
		GPIO.setup(self.v_GPIO_pin, GPIO.OUT)

		# Turn actuator off (cuz it should be "Normally closed")
		GPIO.output(self.v_GPIO_pin, False)

	def turnOn(self, sensor_GPIO_pin):
		if GPIO.input(sensor_GPIO_pin): #Sensor inactive if True	
			GPIO.output(self.v_GPIO_pin, False)
		elif self.v_active:			
			GPIO.output(self.v_GPIO_pin, True)			
	
			if self.v_activation_time>0:
				print "custom activation time =", self.v_activation_time
				time.sleep(self.v_activation_time)
			else:
				print "std activation time = ", sys_config['max_activation_time']
				time.sleep(sys_config['max_activation_time'])

			GPIO.output(self.v_GPIO_pin, False)
		else:
			GPIO.output(self.v_GPIO_pin, False)

		return			

	def turnOff(self, sensor_GPIO_pin):
		GPIO.output(self.v_GPIO_pin, False)			
		return

	def deactivate(self):
		self.v_active = False
		return

	def activate(self):
		self.v_active = True
		return
