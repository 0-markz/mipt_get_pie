import RPi.GPIO as GPIO
import time
leds =  [ 21, 20, 16, 12, 7, 8, 25, 24 ]
dac = [ 26, 19, 13, 6, 5, 11, 9, 10 ]
aux = [ 22,23,27,18,15,14,3,2]


p0 = [0,0,0,0  ,0,0,0,0]
pd = p0
GPIO.setmode(GPIO.BCM)

GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(aux, GPIO.IN)

GPIO.output(leds, p0)
GPIO.output(dac, p0)

while 0==0:
    for i in range(8):
        pd[i] = GPIO.input(aux[i])
    GPIO.output(leds, pd)
    time.sleep(1)
    GPIO.output(leds,p0)

GPIO.output(leds, p0)
GPIO.output(dac, p0)

GPIO.cleanup()