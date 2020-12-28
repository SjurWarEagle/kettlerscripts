import requests
import serial
import time
import telnetlib

port = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
bikespeed = 25
nrRimesInactiveFound = 0
i = 0

print("Starting")
lastspeed = 0
port.write("ID\n".encode())
daten:object = port.readline()
print(daten)
port.write("CD\n".encode())
daten = port.readline()
#print(daten)
port.write("PW 120\r\n".encode())
daten = port.readline()
#print(daten)

def check_setting_active():
    global nrRimesInactiveFound
    if (nrRimesInactiveFound > 0) and (speed > 0):
        print("setting ACTIVE")
        port.write("PW 120\n".encode())
        nrRimesInactiveFound = 0


def check_setting_inactive():
    global daten
    if (nrRimesInactiveFound >= 10):
        print("setting inactive")
        port.write("CM\n".encode())
        daten = port.readline()
        port.write("PT 0\n".encode())
        daten = port.readline()
        port.write("PD 0\n".encode())
        daten = port.readline()
    #        nrRimesInactiveFound=0


def increasingCounters():
    global nrRimesInactiveFound
    if (speed == 0) and (nrRimesInactiveFound <= 10):
        print("inc inactive counter")
        nrRimesInactiveFound = nrRimesInactiveFound + 1


def sendingDataToServer():
    requests.get('http://192.168.73.58:1880/bike?'
                 + 'pulse=' + str(pulse)
                 + '&rpm=' + str(rpm)
                 + '&speed=' + str(speed)
                 + '&power=' + str(power)
                 + '&distance=' + str(distance)
                 + '&energy=' + str(energy)
                 + '&time=' + str((timeTourMin * 60 + timeTourSec))
                 + '&actPower=' + str(actPower)
                 )


while True:
#    print("Loop")
#    print(" Sending ST")
    port.write("ST\n".encode())
#    print(" Reading data")
#    daten = port.read()
    daten = port.readline()
#    print (daten)
    pulse=float(daten[0:3])
    rpm=float(daten[4:7])
    speed=float(daten[8:11])
    distance=float(daten[12:15])/10
    power=float(daten[16:19])
    energy=float(daten[20:24])
    timeTourMin=float(daten[25:27])
    timeTourSec=float(daten[28:30])
    actPower=float(daten[31:34])

    sendingDataToServer()
    increasingCounters()
    check_setting_inactive()
    check_setting_active()

    # print("Debug")
    # print(nrRimesInactiveFound)
    # print(power)
    time.sleep(2)
