import time
from base64 import decode
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code :"+str(rc))
    client.subscribe("#")

def on_message(client, userdata, msg):
    if msg.topic == "Remote/verify":
        if msg.payload.isdigit() and int(msg.payload) < userdata.network.nodeNum:
            client.publish("Remote/"+msg.payload.decode(), payload="Valid", qos=1)
        else:
            client.publish("Remote/"+msg.payload.decode(), payload="Invalid", qos=1)
    print(msg.topic+" "+str(msg.payload))

def bReq_on_message(client, userdata, msg):
    if msg.payload.isdigit():
        inRoute = userdata.addStop(int(msg.payload))
        userdata.addStop(1)
        if inRoute:
            client.publish("Remote/"+msg.payload.decode(), payload="In route", qos=1)
    else: 
        print("Erroneous message sent to BotReq:"+str(msg.payload))
        
def connect(env):
    client = mqtt.Client("Server", userdata=env)
    client.on_connect = on_connect
    client.on_message = on_message
    client.message_callback_add("BotReq", bReq_on_message)
    client.connect("192.168.20.68", 1883)
    return client

def send_update(msg, botNum, client):
    client.publish("Remote/"+str(botNum), payload=msg, qos=1)