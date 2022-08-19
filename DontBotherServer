import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
client = mqtt.Client()


# USER MAINTAINABLE VARIABLES
busy = 20
free = 21
broker_ip = 'pierresensor.local'
broker_port = 1883
mqtt_topic = "meetings/"
mqtt_busy_text = 'busy'
mqtt_free_text = 'free'

def on_message(client, userdata, message):
    outText = message.payload.decode("utf-8")
    print(outText)
    if outText == mqtt_busy_text:
        GPIO.output(free, GPIO.LOW)
        GPIO.output(busy, GPIO.HIGH)
    if outText == mqtt_free_text:
        GPIO.output(busy, GPIO.LOW)
        GPIO.output(free, GPIO.HIGH)

client.on_message=on_message
client.connect(broker_ip, port=broker_port, keepalive=60, bind_address="")
client.subscribe(mqtt_topic)
GPIO.setup(free, GPIO.OUT)
GPIO.setup(busy, GPIO.OUT)

#Flash the LED's to show that the device is on
GPIO.output(busy, GPIO.HIGH)
GPIO.output(free, GPIO.HIGH)
time.sleep(1)
GPIO.output(busy, GPIO.LOW)
GPIO.output(free, GPIO.LOW)
time.sleep(1)

while True:
    client.loop_start()
