'''
Read a sparkfun SEN-10586 weatherboard and write values to a text file with Julian Date CPU clock derived time stamps.

Info on Julian dates:
http://aa.usno.navy.mil/data/docs/JulianDate.php


Example return line from Sparkfun: 
$,80.7,25,43.2,29.986,3.5,10.8,270,0.45,3.90,*


Temp. from humidity sensor, 
Humidity, percent
Dewpoint, 
Barometric pressure,
Relative light level, percent
Wind speed, miles per hour
Wind direction, degrees
Cumulative rainfall, inches
Battery level, volts
* Trailing character (no checksum)

'''

import julian
import math
import functools
import os
import numpy as np
import time
import sys
import serial
import signal
#define sign function for future use:
sign = functools.partial(math.copysign, 1) # http://stackoverflow.com/questions/1986152/why-python-doesnt-have-a-sign-function

port="/dev/ttyUSB1"
cadence=2 #seconds, between sets of reads

print("Cadence: "+str(cadence)+" seconds")
print("ctr-c to quit.")

def sigint_handler(signal,frame):
   #WHAT to do if killed:
    print("SIGINT received! Closing things that might be open...")
    try:
        if not device.closed:
            device.close()
    except Exception, err:
        print(err)

    try:	
        if not fd.closed:
            fd.close()
    except Exception, err:
        print(err)
    print("Exiting.")
    sys.exit(0)
signal.signal(signal.SIGINT,sigint_handler)


try:
    print("trying to initialize device on port: "+port)
    device = serial.Serial(port, 9600, timeout=1)
    print(device)
    device.flushOutput()
    time.sleep(1)

except Exception, err:
    print(err)
    device = False
    print(port+', interface not found.')    
    
def readdvc(device):
    response = device.readline() 
   # 
	#read again if no response:
    if len(response) <1:
	time.sleep(0.1)	
     	response = device.readline() 

    print('-'+response)
    if response[0]=="$":
        weather=np.fromstring(response[1::],sep=",")
        #   print(weather)
        return weather
    else:
        print("invalid return")
        return [False,False]



while True:
    fd = open('weather.txt','a')
    weather=readdvc(device)

    if weather[0]:
        a=np.hstack([julian.jtime(),weather])
    else:
        continue
    np.savetxt(fd,a.reshape(1, a.shape[0]),delimiter=',') #http://stackoverflow.com/questions/9565426/saving-numpy-array-to-txt-file-row-wise
    fd.close()
    time.sleep(cadence)
#
device.close()



