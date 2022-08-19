# DONTBOTHER - A PROJECT BY MILES PUNCH
# A COOL LITTLE PIECE OF SOFTWARE THAT USES MQTT TO TELL PEOPLE IN THE OFFICE TO NOT GO INTO A ROOM.
# USING TKINTER, PAHO-MQTT, AND SOME FANCY REGEX
# AUTOMATICALLY TRIGGERED BY ZOOM, BUT FEATURES A MANUAL OVERRIDE



# IMPORT ALL PACKAGES
from turtle import width
import paho.mqtt.client as mqtt
import time
import os
import re
from tkinter import *

# USER MAINTAINABLE VARIABLES
broker_address = "pierresensor.local"
test_phrase = "No tasks"
broker_port = 1883
mqtt_topic = "meetings/"
mqtt_busy_message = "busy"
mqtt_free_message = "free"
window_title = "Don'tBother"
icon_path = "stop.ico"

# ONE-SHOT VARIABLES
overridebusy = False
overridefree = False
sentOverrideBusy = False
sentOverrideFree = False
sentAutoBusy = False
sentAutoFree = False

# MQTT ON CONNECT CALLBACK
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# THE BIT THAT CHECKS TO SEE IF ZOOM IS RUNNING
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
        # WHEN I WROTE THIS COMMAND, ONLY GOD AND I KNEW HOW IT WORKED, NOW ONLY GOD KNOWS
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

# THE FUNCTION THAT SENDS 'BUSY' TO THE BOX
def imbusy():
    client.publish('meetings/', mqtt_busy_message)

# THE FUNCTION THAT SENDS 'FREE' TO THE BOX
def imfree():
    client.publish('meetings/', mqtt_free_message)

# CHANGES VARIABLES TO SET OVERRIDE TO BUSY
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

# CHANGES VARIABLES TO SET OVERRIDE TO FREE
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

# CHANGES VARIABLES TO CLEAR THE OVERRIDE STATE
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

# SETUP AND DEFINE THE CLIENT
client = mqtt.Client()
client.on_connect = on_connect
client.connect(broker_address,broker_port)

# SETUP AND DEFINE THE Tk WINDOW
root = Tk()
root.geometry("285x480")
root.title(window_title)
root.iconbitmap(icon_path)

# CREATE AND DEFINE THE BUTTONS
button1= Button(root, text="OVERRIDE BUSY", command=overrideBusy, width=40, height=10,bg="#f73131")
button1.grid(row=0,column=0)
button2= Button(root, text="OVERRIDE FREE", command=overrideFree, width=40, height=10,bg="#9df777")
button2.grid(row=1,column=0)
button3= Button(root, text="OVERRIDE CLEAR", command=overrideClear, width=40, height=10,bg="#697780")
button3.grid(row=2,column=0)

# THREAD checkPrograms() and root.mainloop() USING root.after() to keep the back-end alive
root.after(1,checkPrograms)
root.mainloop()