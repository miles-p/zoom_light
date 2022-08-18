from turtle import width
import paho.mqtt.client as mqtt
import time
import os
import re
from tkinter import *

broker_address = "pierresensor.local"
test_phrase = "No tasks"
overridebusy = False
overridefree = False
sentOverrideBusy = False
sentOverrideFree = False
sentAutoBusy = False
sentAutoFree = False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def checkPrograms():
    global sentOverrideBusy
    global sentOverrideFree
    global sentAutoBusy
    global sentAutoFree
    if overridebusy == True and sentOverrideBusy == False:
        print('SENT BUSY')
        imbusy()
        sentOverrideBusy = True
        sentOverrideFree = False
    if overridefree == True and sentOverrideFree == False:
        print('SENT FREE')
        imfree()
        sentOverrideFree = True
        sentOverrideBusy = False
        
    if overridebusy == False and overridefree == False:
        z = os.popen('tasklist /fo table /v /fi "imagename eq CptHost.exe"').read()
        if re.search(test_phrase,z) == None:
            if (sentAutoBusy == False):
                imbusy()
                print('SENT BUSY 2')
                sentAutoBusy = True
                sentAutoFree = False
        else:
            if (sentAutoFree == False):
                imfree()
                print('SENT FREE 2')
                sentAutoFree = True
                sentAutoBusy = False
    root.after(1,checkPrograms)

def imbusy():
    client.publish('meetings/', 'busy')

def imfree():
    client.publish('meetings/', 'free')

def overrideBusy():
    global sentOverrideBusy
    global sentOverrideFree
    global sentAutoBusy
    global sentAutoFree
    global overridebusy
    global overridefree
    overridebusy = True
    overridefree = False
    print("OVERRIDE BUSY", overridebusy)
def overrideFree():
    global overridebusy
    global overridefree
    global sentOverrideBusy
    global sentOverrideFree
    global sentAutoBusy
    global sentAutoFree
    overridefree = True
    overridebusy = False
    print("OVERRIDE FREE", overridefree)
def overrideClear():
    global overridebusy
    global overridefree
    global sentOverrideBusy
    global sentOverrideFree
    global sentAutoBusy
    global sentAutoFree
    overridefree = False
    overridebusy = False
    print("OVERRIDE CLEAR", overridefree, overridebusy)
    sentOverrideBusy = False
    sentOverrideFree = False
    sentAutoBusy = False
    sentAutoFree = False
    checkPrograms()


client = mqtt.Client("P1")
client.on_connect = on_connect
client.connect(broker_address,1883)
root = Tk()
root.geometry("285x480")
root.title("Don'tBother - MQTT Zoom Indicator")

button1= Button(root, text="OVERRIDE BUSY", command=overrideBusy, width=40, height=10,bg="#f73131")
button1.grid(row=0,column=0)
button2= Button(root, text="OVERRIDE FREE", command=overrideFree, width=40, height=10,bg="#9df777")
button2.grid(row=1,column=0)
button3= Button(root, text="OVERRIDE CLEAR", command=overrideClear, width=40, height=10,bg="#697780")
button3.grid(row=2,column=0)

root.after(1,checkPrograms)
root.mainloop()