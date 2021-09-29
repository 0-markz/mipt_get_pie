import RPi.GPIO as GPIO
import time

def dectobin(v, r):
    return [int(bit) for bit in bin(v)[2:].zfill(r)]

def bintodec(binn):
    summ = 0
    bin_t = binn[::-1]
    for i in range(len(bin_t)):
        summ = summ + (2**i)*bin_t[i]
    return summ

def dectodtac(v,r,dac):
    sig = dectobin(v,r)
    GPIO.output(dac, sig)
    time.sleep(0.1)
    return sig

def dtacout(dac, sig,ti):
    GPIO.output(dac, sig)
    time.sleep(ti)
    

def atdc(dac, comp, t):
    dig = [ 0 for _ in dac ]
    for i in range(len(dac)):
        dig[i] = 1
        dtacout(dac, dig, t)
        if GPIO.input(comp):
            dig[i] = 0
        else:
            dig[i] = 1
    return dig
        
    
    
    
    
    
leds =  [ 21, 20, 16, 12, 7, 8, 25, 24 ]

dac  =  [ 26, 19, 13, 6, 5, 11, 9, 10 ]

aux  =  [ 22, 23, 27, 18, 15, 14, 3, 2 ]

trModV = 17

comp = 4
 
mV = 3.3
bits = len(dac)
raz = 2**bits

GPIO.setmode(GPIO.BCM)


GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)


GPIO.setup(trModV, GPIO.OUT, initial = GPIO.HIGH)


GPIO.setup(comp, GPIO.IN)



try:
    while 0==0:
        t = 0.05
        check = 0
        if check == 0:
            print('Do you want to convert analog signal to digital? Type y for yes and  for n')
        inputS = input()
        if inputS == 'y':
            check = 1
            digital = atdc(dac, comp, t)
            print('digital signal', ' '.join(map(str, digital)))
            print('decimal', bintodec(digital))
            volt = ( bintodec(digital) / raz ) * mV
            print('approximate voltage', volt)
            print ('Type y or n')
        elif inputS == 'n':
            break
        else:
            print('Incorrect input, please try again.')
            
except KeyboardInterrupt:
    print("Program was interupted from keyboard")
    
else:
    print("No exceptions happened")
    
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("Done, GPIO cleaned up")