import paho.mqtt.client as mqtt 
import time 

def on_connect(client, userdata, flags, rc):
    print("Connected with result code :"+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    time.sleep(2)
    client.publish("Bot:ec62609270e8", payload="go")

def connect():
    client = mqtt.Client("Remote1")
    client.on_connect = on_connect
    client.on_message = on_message
    client.subscribe("Bot:ec62609270e8")
    client.connect("192.168.20.144", 1883)
    return client