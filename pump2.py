import RPi.GPIO as GPIO
import time

#config
pump_pin = 24
on_duration = 2.5 #seconds (2s=46ml, 2.5s=60ml)

#initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_pin, GPIO.OUT)

def on():
	GPIO.output(pump_pin, True)
	time.sleep(on_duration)
	GPIO.output(pump_pin, False)
	return
on()

GPIO.cleanup()
