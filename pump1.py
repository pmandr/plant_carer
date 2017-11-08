import RPi.GPIO as GPIO
import time

#config
pump_pin = 23
on_duration = 8.5 #seconds (9.6sec~140ml)

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
