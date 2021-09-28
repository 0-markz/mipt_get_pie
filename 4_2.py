import RPi.GPIO as GPIO
import time
def dectobin(v, r):
    return [int(bit) for bit in bin(v)[2:].zfill(r)]
def dectodtac(v,r,dac):
    sig = dectobin(v,r)
    GPIO.output(dac, sig)
    time.sleep(0.01)
    return sig

leds =  [ 21, 20, 16, 12, 7, 8, 25, 24 ]
dac = [ 26, 19, 13, 6, 5, 11, 9, 10 ]
aux = [ 22,23,27,18,15,14,3,2]

mV = 3.3
bits = len(dac)
raz = 2**bits

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)

try:
    while 0==0:
        for v in range(0, 255, 1):
            print("decimal value", dectobin(v, bits))
            print("value", v)
            dectodtac(v, bits, dac)
            volt = (v/raz)*mV
            print("Voltage", volt)
        for v in range(255, 0, -1):
            print("decimal value", dectobin(v, bits))
            print("value", v)
            dectodtac(v, bits, dac)
            volt = (v/raz)*mV
            print("Voltage", volt)
except KeyboardInterrupt:
    print("program was interupted from keyboard")
else:
    print("no exceptions happened")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("done, GPIO cleaned up")