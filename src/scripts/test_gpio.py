#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Simple blink test
for i in range(5):
    GPIO.output(18, True)
    time.sleep(0.5)
    GPIO.output(18, False)
    time.sleep(0.5)
    
GPIO.cleanup()
print("GPIO test completed successfully!")