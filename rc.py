#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 00:36:43 2021

Исследование зависимости напряжениния на конденсаторе от времени

@author: markzaharzevskij
"""

import RPi.GPIO as GPIO
import matplotlib as plt
import pandas as pd
import time

def is_integer(stri):#checking if string can be converted to integer
    try:
        int(stri)
        return True
    except ValueError:
        return False

def dectobin(v, r): #translate a decimal munber into binary, bit quantaty - r
    return [int(bit) for bit in bin(v)[2:].zfill(r)]

def bintodec(binn):#translate a binary number into decimal, 'brute' method
    summ = 0
    #bin_t = binn[::-1]
    for i in range(len(binn)):
        summ = summ*2 + binn[i]
    return summ

def dectodtac(v,r,dac): #supply voltage to dac, argument - decimal 
    sig = dectobin(v,r)
    GPIO.output(dac, sig)
    time.sleep(0.01)
    return sig

def dtacout(dac, sig,ti):#supply voltage to dac, argument - binary
    GPIO.output(dac, sig)
    time.sleep(ti)
    
def ledsindic(leds, sig):#visualization how voltage compares with maximum voltage using leds
    s = [0 for el in sig]#argument - binary
    d = bintodec(sig)
    a = round(8*d/256)
    for i in range(len(s)):
        if i<= a:
            s[i]=1
    GPIO.output(leds,s)

def atdc(dac, comp, t):#atdc, bit method
    dig = [ 0 for _ in dac ]
    for i in range(len(dac)):
        dig[i] = 1
        dtacout(dac, dig, t)
        if GPIO.input(comp):
            dig[i] = 1
        else:
            dig[i] = 0
    return dig
        
    
def atdc2(dac,comp,t): #atdc, linear method
    for i in range(256):
        sig = dectobin(i, 8)
        dtacout(dac, sig, t)
        if (GPIO.input(comp)) == 0:
            return sig
    return sig

def digtoleds(leds, sig):#lighting up leds to represent a binary number
    GPIO.output(leds,sig)

def visualization(df):
    
    df.plot(x='Time', y=['Voltage','Voltagedecimal'], figsize=(10,8), title=r'Voltage on the capacitor')
    plt.xlabel('Time')
    plt.ylabel('Voltage')
    plt.grid(c='#BFEFEF',ls='-',lw=0.5)

def main(iterations):
    leds =  [ 21, 20, 16, 12, 7, 8, 25, 24 ]

    dac  =  [ 26, 19, 13, 6, 5, 11, 9, 10 ]

    trModV = 17

    comp = 4
 
    mV = 3.3
    bits = len(dac)
    maxdec = 2**bits
    
    
    for i in range(iterations):
        print('Starting supply to the capacitor.')
        check = 0
        t=0.01
        GPIO.output(trModV, GPIO.LOW)
        values = []
        times=[]
        voltages=[]
        start_time = time.time()
        while check ==0:
            temp = atdc(dac, comp, t)
            current_time = time.time()
            current_time = current_time - start_time
            value = bintodec(temp)
            digtoleds(leds, temp)
            voltage = (value/maxdec)*mV
            if ((256 - value) < 3 ):
                check = 1
            values.append(value)
            times.append(start_time)
            voltages.append(voltage)
        maxval = value
        charge_time = current_time
        print('The capacitor will discharge now.')
        GPIO.output(trModV, 0)
        while check == 1:
            temp = atdc(dac, comp, t)
            current_time = time.time()
            current_time = current_time - start_time
            value = bintodec(temp)
            digtoleds(leds, temp)
            voltage = (value/maxdec)*mV
            if (value < 3 ):
                check = 0
            values.append(value)
            voltages.append(voltage)
            times.append(start_time)
        discharge_time = current_time
        minval = value
        print('Iteration done.')
        print('Discharge time: '+discharge_time)
        print('Charge time: '+ charge_time)
        print('Total time: ' + (charge_time + discharge_time))
        print('Max voltage, supplied to pin 17' + mV)
        print('Max voltage that was read from the capacitor: decimal ' + maxval + ' volt ' + ((maxval/maxdec)*mV))
        print('Min voltage that was read from the capacitor: decimal ' + minval + ' volt ' + ((minval/maxdec)*mV))
        
        df = pd.DataFrame({'Time': times, 'Voltagedecimal': values, 'Voltage':voltages})
        
        path='values_'+i+'.csv'
        df.to_csv(path,index=False)
        
        dfset = pd.DataFrame({'Charge':charge_time, 'Discharge':discharge_time, 'Stepvolt' : ((1/maxdec)*mV),'Maxvoltdec':maxval, 'Minvoltdec':minval, 'Maxvolt': ((maxval/maxdec)*mV), 'Minvolt': ((minval/maxdec)*mV), 'T': t})
        
        pathset = 'settings_'+i+'.csv'
        dfset.to_csv(pathset, index=False)
        
        visualization(df)
        GPIO.ouput(trModV, GPIO.LOW)
        GPIO.output(dac, GPIO.LOW)
        GPIO.output(leds, GPIO.LOW)
        print('Will continue in 2 seconds.')
        time.sleep(2)
        
        
    
    
    
leds =  [ 21, 20, 16, 12, 7, 8, 25, 24 ]

dac  =  [ 26, 19, 13, 6, 5, 11, 9, 10 ]

aux  =  [ 22, 23, 27, 18, 15, 14, 3, 2 ]

trModV = 17

comp = 4
 
mV = 3.3
bits = len(dac)
maxdec = 2**bits

GPIO.setmode(GPIO.BCM)


GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)

GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)

GPIO.setup(trModV, GPIO.OUT, initial = GPIO.LOW)


GPIO.setup(comp, GPIO.IN)



try:
    check = 0
    iterations = 0
    current_iteration = 0
    while 0==0:
        t = 0.05
        if check == 0:
            print('Greetings! This program requires an RC electric circuit to be connected to RaspberryPie.')
            print('It also would be beneficial if this circuit would be connected to an educational board produced for General Engineering course, since it presumes that it has a comparator, DtAC and etc and the pins for them have already been hardcoded.')
            print('This program will charge the capacitor almost to the full capacity and measure the voltage.')
            print('Then it will allow it to discharge and measure the voltage along the way.')
            print('Do you want to start now? Type y for yes and  for n.')
            inputS = input()
            if inputS == 'y':
                print('Please type in a number representing how many times do You want to conduct the experiment.')
                print('Please keep it between 1 and 10.')
                while check ==0:
                    inputS = input()
                    if is_integer(inputS):
                        if (int(inputS)<0):
                            print('Please enter a positive number.')
                        elif (int(inputS)>10):
                            print('Please enter a lower number.')
                        else:
                            iterations = int(inputS)
                            check = 1
                    else:
                        print('Please enter an integer.')
            elif inputS == 'n':
                break
            else:
                print('Incorrect input, please try again.')
        if check:
            print('Starting.')
            main(iterations)#code here
            print('Do you want to start again? Please type in y/n.')
            print('Warning! This will overwrite target CSV files.')
            inputS = input()
            
            if inputS == 'y':
                check = 0
            elif inputS == 'n':
                break
            else:
                print('Please try again.')
                    
                    
except KeyboardInterrupt:
    print("Program was interupted from keyboard")
    
else:
    print("No exceptions happened")
    
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.cleanup(leds)
    GPIO.cleanup(trModV)
    GPIO.cleanup(comp)
    print("All done, GPIO cleaned up")