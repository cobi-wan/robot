from base64 import decode
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code :"+str(rc))
    client.subscribe("#")

def on_message(client, userdata, msg):
    if msg.topic == "Remote/verify":
        if int(msg.payload) < userdata.network.nodeNum:
            client.publish("Remote/"+msg.payload.decode(), payload="Valid")
        else:
            client.publish("Remote/"+msg.payload.decode(), payload="Invalid")

    if msg.topic == "BotReq":
        pass # On monday add a way to discern the first free bot and send it to the requested node
    print(msg.topic+" "+str(msg.payload))

def connect(env):
    client = mqtt.Client("Server", userdata=env)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.20.68", 1883)
    return client