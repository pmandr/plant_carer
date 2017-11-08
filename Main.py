import RPi.GPIO as GPIO
from Sensor import Sensor
from Actuator import Actuator
import time
import sys

class Main:

	def __init__(self):
		#set parameters
		return

	def run(self):
		while(False):
			time.sleep(1)
			try:
				#start growroom logic here
				pump1 = Actuator(23,'water pump')
				hygrometer1 = Sensor(17,'hygrometer',pump1.turnOn)

			except KeyboardInterrupt:
				print('Interrupted by keyboard \nBye')
				print("Unexpected error:", sys.exc_info()[0])
				return
	
			except:
				print('Other exceptions')
				print("Unexpected error:", sys.exc_info()[0])		
				return
				
			finally:
				GPIO.cleanup()
				return
	

growroom = Main()

#start growroom logic here
pump1 = Actuator(23, 'water_pump',3)
pump2 = Actuator(24, 'water_pump',1)

hygrometer1 = Sensor(17,'hygrometer',pump1.turnOn)
hygrometer2 = Sensor(22,'hygrometer',pump2.turnOn)
#growroom.run()

while True:
	time.sleep(1)
	hygrometer1.getStatus()	
	hygrometer2.getStatus()	

