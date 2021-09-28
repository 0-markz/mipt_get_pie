import RPi.GPIO as GPIO
import time
leds =  [ 21, 20, 16, 12, 7, 8, 25, 24 ]
dac = [ 26, 19, 13, 6, 5, 11, 9, 10 ]

p = [0,1,0,1 , 0,1,0,1]

pd = [1,0,1,0 ,  1,0,1,0]

p0 = [0,0,0,0  ,0,0,0,0]

GPIO.setmode(GPIO.BCM)

GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)

GPIO.output(leds, p)
GPIO.output(dac, pd)

time.sleep(5)


GPIO.output(leds, p0)
GPIO.output(dac, p0)

GPIO.cleanup()