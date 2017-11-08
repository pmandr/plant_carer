import RPi.GPIO as GPIO
import time

#config
light_pin = 4
on_duration = 12*3600 #12 hours
off_duration = 12*3600-5 #12 hours

#initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(light_pin, GPIO.OUT)

def on():
	GPIO.output(light_pin, True)
	time.sleep(on_duration)
	return

def off():
	GPIO.output(light_pin, False)
	time.sleep(off_duration)
	return

on()
off()

GPIO.cleanup()
