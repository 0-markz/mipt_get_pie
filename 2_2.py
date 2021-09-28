import RPi.GPIO as GPIO
import time
leds =  [ 21, 20, 16, 12, 7, 8, 25, 24 ]
dac = [ 26, 19, 13, 6, 5, 11, 9, 10 ]

#p = [0,1,0,1 , 0,1,0,1]

#pd = [1,0,1,0 ,  1,0,1,0]

p0 = [0,0,0,0  ,0,0,0,0]

GPIO.setmode(GPIO.BCM)

GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)

period = int(input())
GPIO.output(leds, p0)
GPIO.output(dac, p0)


while 0==0:
    for i in range(8): #082
        GPIO.output(dac[i],1)
        #GPIO.output(dac[i+1],1)
        time.sleep(period)
        GPIO.output(leds, p0)
        GPIO.output(dac, p0)




GPIO.output(leds, p0)
GPIO.output(dac, p0)

GPIO.cleanup()