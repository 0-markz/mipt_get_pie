#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 23:57:18 2021

@author: markzaharzevskij
"""

def dectobin(v, r):
    return [int(bit) for bit in bin(v)[2:].zfill(r)]

def bintodec(binn):
    summ = 0
    bin_t = binn[::-1]
    for i in range(len(bin_t)):
        summ = summ + (2**i)*bin_t[i]
    return summ

def atdc(dac, comp, t):
    dig = [ 0 for _ in dac ]
    for i in range(len(dac)):
        print('dig')
        print(' '.join(map(str,dig)))
        #temp = dig
        #temp[i] = 1
        #print('temp')
        #print(' '.join(map(str,temp)))
        #dtacout(dac, dig, t)
        if comp[i]:
            dig[i] = 1
    return dig


#testing some stuff to be completly sure it works

dac  =  [ 26, 19, 13, 6, 5, 11, 9, 10 ]

#print (' '.join(map(str, dac)))

#n = int(input())


#print ((dectobin(n, 8)))
#print(bintodec(dectobin(n,8)))
comp = [ 0, 1, 0, 0, 1, 1, 0, 1]
print(' '.join(map(str, atdc(dac, comp, 0.1))))