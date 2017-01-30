import RPi.GPIO as GPIO
from sys_config import sys_config
import time

# Set our GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

class Sensor:

	def __init__(self, in_GPIO_pin, in_type, in_callback_function = None):
		self.v_GPIO_pin = in_GPIO_pin
		self.v_callback_function = in_callback_function
		self.v_type = in_type

		# Set the GPIO pin to an input
		GPIO.setup(self.v_GPIO_pin, GPIO.IN)

		if callable(self.v_callback_function):
			self.watch()
		else:		
#			GPIO.setup(self.v_GPIO_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
			self.v_cur_status = getStatus()		

	def watch(self):
		# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
		GPIO.add_event_detect(self.v_GPIO_pin, GPIO.BOTH, bouncetime=300)
		# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
		GPIO.add_event_callback(self.v_GPIO_pin, self.v_callback_function)
			
		time.sleep(sys_config['min_sensor_interval'])
	
		print "watching..."
		return

	def getStatus(self):
		self.v_cur_status = GPIO.input(self.v_GPIO_pin)				
		print "getStatus = ", self.v_cur_status
		return self.v_cur_status
