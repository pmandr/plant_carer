import RPi.GPIO as GPIO
import time

#config
light_pin = 4
on_duration = 18*3600 #18 hours
off_duration = 6*3600 #6 hours
file = open('./growroom101.log','w+')

#initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(light_pin, GPIO.OUT)

def on():
	GPIO.output(light_pin, True)
	message = "Lights On! Started at: "+time.ctime()+'\n'
	print message
	file.write(message)
	time.sleep(on_duration)
	return

def off():
	GPIO.output(light_pin, False)
	message = "Lights Off! Started at: "+time.ctime()+'\n'
	print message
	file.write(message)
	time.sleep(off_duration)
	return

while True:
	on()
	off()

GPIO.cleanup()
