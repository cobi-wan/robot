import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code :"+str(rc))

def nodeSubscription(client, userdata, msg):
    if msg.payload == b'In route':
        print("Bot in route")
        userdata.inRoute = True
    elif msg.payload == b'Arrived':
        print("Bot arrived")
        userdata.inRoute = False
    else: 
        print(msg.topic+" "+str(msg.payload))

def subCheck(client, userdata, msg):
    userdata.msgReceived = True
    print("Uh oh")
    if msg.payload == b'Valid':
        userdata.valid = True
        print("connected at ", str(userdata.nodeNum))
    else:
        print("Not a valid node")
        client.unsubscribe("Remote/"+str(userdata.nodeNum))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def connect():
    client = mqtt.Client("Remote1")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.20.68", 1883)
    return client

def assign_location(client):
    # Connect at a user specified node
    client._userdata.reset()
    while not client._userdata.valid:
        nodeNum = input("Please enter the node number that this process is running at: ")
        client._userdata.nodeNum = nodeNum
        client.message_callback_add("Station/"+str(nodeNum), subCheck)
        client.subscribe("Station/"+str(nodeNum))
        client.publish("Station/verify", payload=str(nodeNum))
        time.sleep(1)
        while not client._userdata.msgReceived:
            pass
    client.message_callback_add("Remote/"+str(nodeNum), nodeSubscription)