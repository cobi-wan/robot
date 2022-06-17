import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code :"+str(rc))
    client.subscribe("#")

def on_message(client, userdata, msg):
    if msg.topic == "Remote/enter":
        nodeNum = input(msg.payload)
    if str(msg.payload) == "b'server connection initialized...'":
        time.sleep(2)
        client.publish("Test", "Send back")
    print(msg.topic+" "+str(msg.payload))

def connect():
    client = mqtt.Client("Paho")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.20.68", 1883)
    return client