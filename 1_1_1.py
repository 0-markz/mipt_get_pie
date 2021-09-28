import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(15, GPIO.IN)
temp = GPIO.input(15)
sost = 0
while 0==0:
    if temp != GPIO.input(15):
        if temp == 0:
            if sost ==1:
                sost = 0
            else:
                sost =1
        temp = GPIO.input(15)
    GPIO.output(3, sost)
    time.sleep(1)